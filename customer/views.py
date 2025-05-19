from typing import Any, Dict
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from shop.models import * 
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django import http, template
from shop.mixins import *
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from . import forms
from django import template
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
# Create your views here.

register = template.Library()

@register.filter
def zip_lists(a, b):
    return zip(a, b)

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


class ProductDetailView(DetailView):
    model = Products
    template_name = 'customer/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        imgs = context['product'].product_images.all()
        context['imgs'] = imgs
        
        context['product'].price = f'{context["product"].price:,}'.replace(',', ' ') 

        context['reviews'] = context['product'].reviews.all()

        

        return context   
    
class BusketDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shop.view_baskets'
    model = Baskets
    template_name = 'customer/basket_detail.html'
    context_object_name = 'basket'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        context = super().get_context_data(**kwargs)

        products = context['basket'].products.all()
        print(products)
        products_images = []
        for product in products:
            
            imgs = product.product_images.all()
            
            for img in imgs:
                
                if img.is_primary:
                    products_images.append(img)
                    
            
        context['combined'] = zip_lists(products, products_images)

        return context

class AddProductToBusketView(PermissionRequiredMixin, View):
    permission_required = 'shop.add_product_to_busket'
    
   
    def get(self, request, pk, *args, **kwargs):
        
        basket = request.user.basket
        
        product = Products.objects.filter(pk = self.kwargs['pk']).first()
        
        basket.products.add(product)
        
        return HttpResponseRedirect(reverse_lazy('basket_detail', kwargs={'pk' : basket.pk}))

class CreateOrderView(PermissionRequiredMixin, View):
    permission_required = 'shop.add_orders'
    
    def get(self, request, *args, **kwargs):
        basket = request.user.basket
        products = basket.products.all()
        quantity = 1
        total_price = 0
        
        order = Orders(user = request.user)
        order.save()
        for product in products:
            order_item = OrderItems(order = order, product = product, quantity = quantity)
            order_item.save()
            total_price += product.price * quantity
            order.order_items.add(order_item)
            
        
        order.total_price = total_price
        order.save()
        basket.products.clear()
        
        return HttpResponseRedirect(reverse_lazy('basket_detail', kwargs = {'pk':basket.pk}))
        
class OrdersListView(PermissionRequiredMixin, ListView):
    permission_required = 'shop.view_orders'
    template_name = 'customer/orders.html'
    context_object_name = 'orders'
    model = Orders
        
class OrderItemsListView(PermissionRequiredMixin, ListView):
    permission_required = 'shop.view_orderitems'
    model = OrderItems
    template_name = 'customer/order_items.html'
    context_object_name = 'order_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        

        order = Orders.objects.filter(pk = self.kwargs['order_pk']).first()
        context['order'] = order

        context['order_items'] = OrderItems.objects.filter(order = order).all()

        products = []
        for item in context['order_items']:
            products.append(item.product)

        
        products_images = []
        for product in products:
            
            imgs = product.product_images.all()
            
            for img in imgs:
                
                if img.is_primary:
                    products_images.append(img)
                    
        
        context['combined'] = zip_lists(products, products_images)

        return context

class CreateReviewView(CreateView):
    permission_required = 'shop.can_add_review'
    form_class = forms.CreateReviewForm
    model = Reviews
    template_name = 'customer/create_review.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comment_form'] = forms.CreateCommentForm()

        return context
    def post(self, request, *args, **kwargs):
        comment_form = forms.CreateCommentForm(request.POST, request.FILES)
        review_form = forms.CreateReviewForm(request.POST, request.FILES)
        if comment_form.is_valid() and review_form.is_valid():
            comment = comment_form.save(commit=False)
            review = review_form.save(commit=False)
            
            review.user = request.user
            comment.author = request.user
            review.product = Products.objects.filter(pk = self.kwargs['product_pk']).first()
            review.comment = comment
            comment.save()
            review.save()

        return redirect('product', pk = self.kwargs['product_pk'])