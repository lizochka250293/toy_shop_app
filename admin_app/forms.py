from app_toy_shop.models import Product
from django import forms

class ProductDetailForm(forms.ModelForm):


    class Meta:
        model = Product
        fields = ["name", "description", "price", "poster", "category", "quantity", "is_active"]
