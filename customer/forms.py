from django import forms
from shop.models import *



class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['rating']
        widgets = {'rating' : forms.NumberInput(attrs = {
            'class' : 'form-control',
            'min': '1',
            'placeholder': 'Введіть кількість'
        })}

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text' : forms.Textarea(attrs = {
            'class' : 'form-control',
            'placeholder': 'Ваш відгук'
        })}