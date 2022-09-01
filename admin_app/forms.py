from django import forms

from app_toy_shop.models import Product


class ProductDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    description = forms.Textarea(attrs={'colm': 60, 'rows': 10})

    class Meta:
        model = Product
        fields = ["name", "description", "price", "poster", "category", "quantity", "is_active"]


class StocksForm(forms.Form):
    title = forms.CharField(label='Акция', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
