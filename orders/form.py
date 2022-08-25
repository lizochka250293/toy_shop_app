from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    address = forms.CharField(label='Адрес')
    city = forms.CharField(label='Город')

    class Meta:
        model = Order
        fields = ['address', 'city', 'paid']


class AddPayForm(forms.Form):
    number_card = forms.CharField(label='Номер карты', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    date = forms.CharField(label='Срок действия', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    csv = forms.CharField(label='csv код', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    user = forms.CharField(label='Пользователь', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))


class OrderListForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']
