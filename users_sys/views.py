from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginUserForm
from django.contrib.auth import login

# Create your views here.
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users_sys/register.html'

    
    
   

class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users_sys/login.html'
    success_url = reverse_lazy('home')

