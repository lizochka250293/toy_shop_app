from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    address = forms.CharField(label='Адрес')
    city = forms.CharField(label='Город')

    class Meta:
        model = Order
        fields = ['address', 'city', 'paid']


class AddPayForm(forms.Form):
    number_card = forms.CharField(label='Номер карты', widget=forms.Textarea(attrs={'cols': 10, 'rows': 2}))
    date = forms.CharField(label='Срок действия', widget=forms.Textarea(attrs={'cols': 10, 'rows': 2}))
    csv = forms.CharField(label='csv код', widget=forms.Textarea(attrs={'cols': 10, 'rows': 2}))
    user = forms.CharField(label='Пользователь', widget=forms.Textarea(attrs={'cols': 10, 'rows': 2}))


class OrderListForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']
