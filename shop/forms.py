from django import forms
from .models import *

class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['status']
        widgets = {
            'status' : forms.Select(
            attrs={
                'class' : 'form-control'
            })
        }

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
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'category' : forms.Select(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'price' : forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'character' : forms.Textarea(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'description' : forms.Textarea(
                attrs={
                    'class' : 'form-control'
                }
            )
        }

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'category', 'price', 'availability', 'character', 'description']
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'category' : forms.Select(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'price' : forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'character' : forms.Textarea(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'description' : forms.Textarea(
                attrs={
                    'class' : 'form-control'
                }
            )
        }

class CreateProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image', 'is_primary']
        widgets = {
            'image' : forms.FileInput(
                attrs={
                    'class' : 'form-control'
                }
            ),
            
        }
    
ProductImageFormSet = forms.inlineformset_factory(
    Products, ProductImages, form=CreateProductImageForm,
    extra=1, can_delete=True
)


class CreateDiscountForm(forms.ModelForm):
    class Meta:
        model = Discounts
        fields = ['discount_percentage', 'start_date','end_date']
        widgets = {
            'start_date':forms.TextInput(attrs={
            'type':'datetime-local', 
            'class': 'form-control'
            }), 
            'end_date':forms.TextInput(attrs={
                'type':'datetime-local',
                'class': 'form-control'
            }),
            'discount_percentage' : forms.NumberInput(attrs={
            'class' : 'form-control'
            })}