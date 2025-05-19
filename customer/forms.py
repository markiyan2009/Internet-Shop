from django import forms
from shop.models import *



class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['rating']

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']