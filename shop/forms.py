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
