from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from orders.models import Order
from user.models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя')
    phone = forms.CharField(label='Телефон')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повтор пароля')

    class Meta:
        model = User
        fields = ('username', 'phone', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class OrderUserForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']
