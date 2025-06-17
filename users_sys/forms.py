from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomerProfile, ShopProfile
from django.contrib.auth import get_user_model

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Login",widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_shop = forms.BooleanField(label='Чи це магазин?', initial=False, required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'is_shop']

class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = models.ShopProfile
        fields = ['name', 'logo','description']  
        widgets = {
            'logo' : forms.FileInput(attrs={
                'class' : 'form-control'
            }),
            'description' : forms.Textarea(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'name' : forms.TextInput(
                attrs={
                    'class' : 'form-control'
                }
            )
        }  

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = models.CustomerProfile
        fields = ['photo', 'adress', 'phone_number']
        widgets = {
            'photo' : forms.FileInput(attrs={
                'class' : 'form-control'
            }),
            'adress' : forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'phone_number' : forms.TextInput(
                attrs={
                    'class' : 'form-control'
                }
            )
        }
