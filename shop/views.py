from typing import Any, Dict
from django.forms.models import BaseModelForm
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
from cloudinary.uploader import upload, destroy



# Create your views here.

register = template.Library()

@register.filter
def zip_lists(a, b):
    return zip(a, b)

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

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
        
        return context
    

    
class UpdateOrderStatusView(PermissionRequiredMixin, UpdateView):
    permission_required = 'shop.change_orders'
    form_class = forms.UpdateOrderStatusForm
    template_name = 'shop/update_order_status.html'
    model = Orders
    
    def get_success_url(self) -> str:
        return reverse_lazy('orders_manager', kwargs = {'user_pk':self.request.user.pk})
    
      




class OrderListManagerView(PermissionRequiredMixin, ListView):
    permission_required = 'shop.change_orders'
    template_name = 'shop/orders_manager.html'
    model = Orders
    context_object_name = 'orders'  

class ProductShopListView(ListView):
    # permission_required = None
    model = Products
    context_object_name = 'products'
    template_name = 'shop/products.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        products = self.request.user.shop_profile.products.all()
        
        products_images = []
        for product in products:
            
            imgs = product.product_images.all()
            
            for img in imgs:
                
                if img.is_primary:
                    products_images.append(img)
                    
            
        context['combined'] = zip_lists(products, products_images)

    
        return context
    
class ShopProductView(PermissionRequiredMixin, UpdateView):
    permission_required = 'shop.change_products'
    form_class = forms.UpdateProductForm
    template_name = 'shop/product.html'
    model = Products
    success_url = reverse_lazy('shop_products')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Products.objects.filter(pk = self.kwargs['pk']).first()
        product_images = product.product_images.all()
       
        
        # img_forms = []
        # for img in product_images:
        #     form = forms.UpdateProductImagesForm(initial={'image':img})
        #     img_forms.append(form)

        # context['img_forms'] = img_forms
        context['imgs'] = product_images
        return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         product = self.get_object()
#         product_form = self.get_form()
#         img_forms = [forms.UpdateProductImagesForm(request.POST, prefix=str(i)) for i in range(3)]
#         product_images = product.product_images.all()
#         all_valid = product_form.is_valid() and all(f.is_valid() for f in img_forms)
#         image_fields = []
#         for i in range(len(product_images)):
#             image_fields.append(F'image_{i}')
        
# # доробити
#         if all_valid:
#             product_form.save()
#             for i in range(len(product_images)):
#                 old_img = product_images[i]
#                 img = img_forms[i].cleaned_data["image"]
#                 field_name = image_fields[i]

#                 if old_img:
#                     destroy(old_img.public_id)
#                 uploaded = upload(img)
#                 setattr(self.object, field_name, uploaded['public_id'])
#                 img_forms[i].save()
#             self.object.save()
#         return redirect(self.get_success_url())
                
class CreateDiscountView(CreateView):
    model = Discounts
    form_class = forms.CreateDiscountForm
    template_name = 'shop/create_discount.html'
    success_url = reverse_lazy('shop_products')

    def form_valid(self, form):
        product = Products.objects.filter(pk = self.kwargs['pk']).first()
        form.instance.product = product
        discount = form.save()
        product.discount = discount
        
        product.save()
        return super().form_valid(form)