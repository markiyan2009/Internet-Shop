from typing import Any, Dict
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from shop.models import * 
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django import http, template
from shop.mixins import *
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect

# Create your views here.

register = template.Library()

@register.filter
def zip_lists(a, b):
    return zip(a, b)

class HomeView(ListView):
    model = Products
    template_name = 'shop/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Products.objects.all()

        context['loops'] = len(products)
        products_images = []
        for product in products:
            
            imgs = product.product_images.all()
            
            for img in imgs:
                
                if img.is_primary:
                    products_images.append(img)
                    
            print(products_images)
        context['combined'] = zip_lists(products, products_images)
        # if self.request.user.customer_profile is not None:
        #     print('customer')
        # if self.request.user.shop_profile is not None:
        #     print('huy')

        return context
    
class ProductDetailView(DetailView):
    model = Products
    template_name = 'shop/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        imgs = context['product'].product_images.all()
        context['imgs'] = imgs
        
        context['product'].price = f'{context["product"].price:,}'.replace(',', ' ') 

        context['reviews'] = context['product'].reviews.all()


        return context   
    
class BusketDetailView(DetailView):
    model = Baskets
    template_name = 'shop/basket_detail.html'
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

class AddProductToBusketView(View):
    def get(self, request, pk, *args, **kwargs):
        
        basket = request.user.basket
        
        product = Products.objects.filter(pk = self.kwargs['pk']).first()
        
        basket.products.add(product)
        
        return HttpResponseRedirect(reverse_lazy('basket_detail', kwargs={'pk' : basket.pk}))

class CreateOrderView(View):
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
        
        return HttpResponseRedirect(reverse_lazy('basket_detail', kwargs = {'pk':basket.pk}))
        
class OrdersListView(ListView):
    template_name = 'shop/orders.html'
    context_object_name = 'orders'
    model = Orders
        
class OrderItemsListView(ListView):
    model = OrderItems
    template_name = 'shop/order_items.html'
    context_object_name = 'order_items'

    