from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomerProfile, ShopProfile
from django.contrib.auth import get_user_model

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                    widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",
                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    is_shop = forms.BooleanField(label='Чи це магазин?', initial=False, required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'is_shop']

class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = models.ShopProfile
        fields = ['logo','description']    

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = models.CustomerProfile
        fields = ['photo', 'adress', 'phone_number']
