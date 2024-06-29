from django import forms
from .models import Product, Order
from datetime import date


class ProductForm(forms.ModelForm):   

   class Meta:
      model=Product
      fields=['description','category','price','quantity','photo_url']
      
      
'''for testing order months purpose'''
class OrderForm(forms.ModelForm):
    placed_order_at = forms.DateTimeField(
        widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )

    class Meta:
        model = Order
        fields = '__all__'