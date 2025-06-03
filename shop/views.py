from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from shop.models import * 
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View, TemplateView
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

# class HomeView(ListView):
#     model = Products
#     template_name = 'shop/home.html'
#     context_object_name = 'products'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         products = Products.objects.all()

#         context['loops'] = len(products)
#         products_images = []
#         for product in products:
            
#             imgs = product.product_images.all()
            
#             for img in imgs:
                
#                 if img.is_primary:
#                     products_images.append(img)
                    
#             print(products_images)

#         # context['categories'] = Categories.objects.all()
#         context['combined'] = zip_lists(products, products_images)
        
#         return context
class HomeView(View):
    def get(self, request):
        context = {}
        categories = Categories.objects.all()
        products = Products.objects.all()
    
        context['loops'] = len(products)
        products_images = []
        for product in products:
            product.price =  product.formatted_price
            imgs = product.product_images.all()
            
            for img in imgs:
                
                if img.is_primary:
                    products_images.append(img)
                    
            print(products_images)

        context['categories'] = categories
        context['combined'] = zip_lists(products, products_images)

        


        return render(request, 'shop/home.html', context=context)
    
class HomeCategoriesView(View):
    def get(self, request):
        category_id = request.GET.get('category')
        search_query = request.GET.get('search')

        products = Products.objects.all()

        if category_id:
            products = products.filter(category_id=category_id)

        if search_query:
            products = products.filter(name__icontains=search_query)

        data = [
            {
                'name': item.name,
                'pk': item.pk,
                'price': item.formatted_price,
                'availability': item.availability,
                'character': item.character,
                'description': item.description,
                'image_url': item.product_images.filter(is_primary=True).first().image.url
                    if item.product_images.filter(is_primary=True).exists() else ''
            }
            for item in products
        ]

        return JsonResponse({"results": data})
    
    
    
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
    
        context['imgs'] = product_images
        return context

                
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

# class UpdateProductImagesView(UpdateView):
#     permission_required = 'shop.change_productimages'
#     model = ProductImages
#     form_class = None

class CreateProductView(View):
    def get(self, request):
        pass

def create_product(request):
    if request.method == 'POST':
        form = forms.CreateProductForm(request.POST)
        formset = forms.ProductImageFormSet(request.POST, request.FILES, prefix='images')
        if form.is_valid() and formset.is_valid():
            shop_profiles = ShopProfile.objects.all()
            auth = request.user
            form.instance.shop = auth.shop_profile
            
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect('shop_products')  # або інша твоя сторінка
    else:
        form = forms.CreateProductForm()
        formset = forms.ProductImageFormSet(prefix='images')


    return render(request, 'shop/create_product.html', {'form': form, 'formset': formset})