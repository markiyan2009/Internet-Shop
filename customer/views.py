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
from django.core.exceptions import PermissionDenied
from collections import Counter
# Create your views here.

register = template.Library()

@register.filter
def zip_lists(*args):
    return zip(*args)

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
        all_products = Products.objects.all()
        basket_items = context['basket'].items.all()
        product_ids = basket_items.values_list('product_id', flat=True)
        products = Products.objects.filter(id__in=product_ids)
        print(products)
        
        products_images = []
        for product in products:
            product.price =  product.formatted_price
            imgs = product.product_images.all()
            
            for img in imgs:
                
                if img.is_primary:
                    products_images.append(img)
                    
            
        context['combined'] = zip_lists(products, products_images, basket_items)
    
        return context

class AddProductToBusketView(PermissionRequiredMixin, View):
    permission_required = 'shop.add_product_to_busket'
    
   
    def get(self, request, pk, *args, **kwargs):
        
        basket = request.user.basket
        
        product = Products.objects.filter(pk = self.kwargs['pk']).first()
        
        item = ItemBasket.objects.create(basket= basket, product = product)
        item.save()
        

        
        return HttpResponseRedirect(reverse_lazy('basket_detail', kwargs={'pk' : basket.pk}))

class ActionProductQuantityView(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print('get')
            basket = Baskets.objects.filter(pk = self.kwargs['pk']).first()
            for item in basket.items.all():
                btn_action = request.POST.get('action')
                if btn_action == f'add-btn-{item.pk}':
                
                    item.quantity += 1
                    item.save()
                elif btn_action == f'minus-btn-{item.pk}':
                    if item.quantity >1:
                        item.quantity -= 1
                        item.save()
        return HttpResponseRedirect(reverse_lazy('basket_detail', kwargs={'pk' : basket.pk}))

class CreateOrderView(PermissionRequiredMixin, View):
    permission_required = 'shop.add_orders'
    
    def get(self, request, *args, **kwargs):
        basket = request.user.basket
        basket_items = basket.items.all()
        product_ids = basket_items.values_list('product_id', flat=True)
        products = Products.objects.filter(id__in=product_ids)
        
        product_counts = Counter(products)  # <--- Оце головне

        total_price = 0
        order = Orders(user=request.user)
        order.save()

        for product, item in zip(products, basket_items):
            order_item = OrderItems(order=order, product=product, quantity= item.quantity)
            order_item.save()

            if product.discount:
                total_price += product.price_with_discount * item.quantity
            else:
                total_price += product.price * item.quantity

            order.order_items.add(order_item)

        order.total_price = total_price
        order.user = request.user
        order.save()
        basket.items.all().delete()  # очищення кошика

        return redirect('basket_detail', pk=basket.pk)
        
class OrdersListView(PermissionRequiredMixin, ListView):
    permission_required = 'shop.view_orders'
    template_name = 'customer/orders.html'
    context_object_name = 'orders'
    model = Orders

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        orders = Orders.objects.filter(user = self.request.user).all()
        context['orders'] = orders
        colors = []
        for order in context['orders']:
            if order.status == 'received':
                colors.append('rgb(0, 121, 1)')
            elif order.status == 'canceled':
                colors.append('red')
            else:
                colors.append('black')
        
        context['combined'] = zip(orders, colors)
        return context
        
class OrderItemsListView(PermissionRequiredMixin, ListView):
    permission_required = 'shop.view_orderitems'
    model = OrderItems
    template_name = 'customer/order_items.html'
    context_object_name = 'order_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        

        order = Orders.objects.filter(pk = self.kwargs['order_pk']).first()

        order.total_price = f'{order.total_price:,.2f}'.replace(',', ' ').replace('.00', '')

        if order.status == 'received':
            context['color'] = 'rgb(0, 121, 1)'
        elif order.status == 'canceled':
            context['color'] = 'red'

        context['order'] = order

        context['order_items'] = OrderItems.objects.filter(order = order).all()

        products = []
        for item in context['order_items']:
            products.append(item.product)

        
        products_images = []
        for product in products:
            # тут форматувати ціну !!!!!!!!!!!!
            product.price =  product.formatted_price
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

class CategoriesListViews(ListView):
    model = Categories
    template_name = 'customer/categories.html'
    context_object_name = 'categories'

class PermCreateReviewView(View):
    def get(self, request, pk):
        # has_perm = request.user.has_perm('shop.add_review_who_but_it') 

        product = Products.objects.filter(pk = pk).first()
        has_perm = OrderItems.objects.filter(order__user= request.user,   order__status='received', product=product).exists()
        print(has_perm)
        return JsonResponse({'has_perm': has_perm})
    
class DeleteReviewView(DeleteView):
    model = Reviews
    template_name = 'customer/delete_review.html'
    success_url = reverse_lazy('home')

class DeleteItemBusketView(DeleteView):
    model = ItemBasket
    template_name = 'customer/delete_item_basket.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        item = ItemBasket.objects.filter(pk = self.kwargs['pk']).first()
        if item.basket.user != request.user:
            return PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        item = ItemBasket.objects.filter(pk=self.kwargs['pk']).first()
        context['name'] = item.product.name
        context['basket_pk'] = item.basket.pk
        return context
    def get_success_url(self) -> str:
        basket = ItemBasket.objects.filter(pk = self.kwargs['pk']).first().basket
        return reverse_lazy('basket_detail', kwargs={'pk': basket.pk})
    

class CancelOrderView(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        order = Orders.objects.filter(pk = self.kwargs['pk']).first()
        if order.user != request.user and order.status == 'framed':
            return PermissionDenied
        else:
            order.status = 'canceled'
            order.save()
        return HttpResponseRedirect(reverse_lazy('orders_list', kwargs={'user_pk' : request.user.pk}))
    