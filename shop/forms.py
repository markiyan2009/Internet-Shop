from django import forms
from .models import Products

class AddToCartForm(forms.ModelForm):
    model = Products
    #модель айтема кошику, реєстрація і логін
    fields = ['']