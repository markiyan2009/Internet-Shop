from django import forms
from .models import *

class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['status']

class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['rating']

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'availability', 'character', 'description']

class UpdateProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image']

class CreateDiscountForm(forms.ModelForm):
    class Meta:
        model = Discounts
        fields = ['discount_percentage', 'start_date','end_date']
        widgets = {'start_date':forms.TextInput(attrs={'type':'datetime-local'}), 'end_date':forms.TextInput(attrs={'type':'datetime-local'})}