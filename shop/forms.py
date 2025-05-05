from django import forms
from .models import *

class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['status']