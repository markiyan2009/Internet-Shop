from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginUserForm, ShopProfileForm, CustomerProfileForm
from django.contrib.auth import login
from users_sys import models
from shop import models as shop_models
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
import cloudinary

customer_group = Group.objects.get(name='customer') 
shop_group = Group.objects.get(name='magazine') 
# Create your views here.
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users_sys/register.html'

    def form_valid(self, form):
        is_shop = form.cleaned_data['is_shop']



        self.request.session['is_shop'] = is_shop
        self.request.session.save()

        

        user = form.save()

        if is_shop:
            user.groups.add(shop_group)
        else:
            shop_models.Baskets.objects.create(user = user)
            user.groups.add(customer_group)
        login(self.request, user)
        return super().form_valid(form)
        
    def get_success_url(self) -> str:
        
        
        if self.request.session.get('is_shop'):
            return reverse_lazy('shop_profile_create')
        else:

            return reverse_lazy('customer_profile_create')
        
    
   

class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users_sys/login.html'
    success_url = reverse_lazy('home')


class CreateShopProfileView(PermissionRequiredMixin, CreateView):
    permission_required = 'users_sys.add_shopprofile'
    form_class = ShopProfileForm
    template_name = 'users_sys/profile_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
    
class CreateCustomerProfileView(PermissionRequiredMixin, CreateView):
    permission_required = 'users_sys.add_customerprofile'
    form_class = CustomerProfileForm
    template_name = 'users_sys/profile_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
      
        return super().form_valid(form)
    
class DetailShopProfileView(PermissionRequiredMixin, DetailView):
    permission_required = 'users_sys.view_shopprofile'
    model = models.ShopProfile
    template_name = 'users_sys/detail_shop_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user.shop_profile.pk)
        return context

class DetailCustomerProfileView(PermissionRequiredMixin, DetailView):
    permission_required = 'users_sys.view_customerprofile'
    model = models.CustomerProfile
    template_name = 'users_sys/detail_customer_profile.html'
    context_object_name = 'profile'

class UpdateCustomerProfile(PermissionRequiredMixin, UpdateView):
    permission_required = 'users_sys.change_customerprofile'
    model = models.CustomerProfile
    template_name = 'users_sys/update_profile.html'
    form_class = CustomerProfileForm
    

    def form_valid(self, form):
        profile = models.CustomerProfile.objects.filter(pk = self.kwargs['pk']).first()
       
        if form.instance.photo and profile.photo:
            cloudinary.uploader.destroy(profile.photo.public_id)
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('customer_detail', kwargs = {'pk': self.kwargs['pk']})
    
class UpdateShopProfile(PermissionRequiredMixin, UpdateView):
    permission_required = 'users_sys.change_shopprofile'
    model = models.ShopProfile
    template_name = 'users_sys/update_profile.html'
    form_class = ShopProfileForm

    def form_valid(self, form):
        profile = models.ShopProfile.objects.filter(pk = self.kwargs['pk']).first()
       
        if form.instance.logo and profile.logo:
            cloudinary.uploader.destroy(profile.logo.public_id)
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('customer_detail', kwargs = {'pk': self.kwargs['pk']})
    
    def get_success_url(self) -> str:
        return reverse_lazy('shop_detail', kwargs = {'pk': self.kwargs['pk']})