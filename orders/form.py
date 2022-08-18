from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):

    # user = forms.CharField(label='Пользователь')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['user'].label = "Пользователь"
        self.fields['user'].empty_label = self.request.user

    class Meta:
        model = Order
        fields = ['user', 'address', 'city', 'paid']
