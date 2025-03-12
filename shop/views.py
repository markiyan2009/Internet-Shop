from typing import Any, Dict
from django.shortcuts import render

from shop.models import * 
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django import template



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
        context['products_images'] = products_images
        context['combined'] = zip_lists(products, products_images)
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