from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):

    address = forms.CharField(label='Адрес')
    city = forms.CharField(label='Город')

    class Meta:
        model = Order
        fields = ['address', 'city', 'paid']


class AddPayForm(forms.Form):
    number_card = forms.IntegerField(label='Номер карты')
    date = forms.CharField(label='Срок действия', max_length=255)
    csv = forms.IntegerField(label='csv код')
    user = forms.CharField(label='Пользователь', max_length=255)


class OrderListForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['order_status']

