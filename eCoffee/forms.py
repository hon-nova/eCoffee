from django import forms
from .models import Product
from datetime import date


class ProductForm(forms.ModelForm):   

   class Meta:
      model=Product
      fields=['description','category','price','quantity','photo_url']