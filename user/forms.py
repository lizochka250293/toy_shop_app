from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from user.models import User
from user.validators import phone_validator
from django import forms

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя')
    phone = forms.CharField(label='Телефон')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повтор пароля')

    class Meta:
        model = User
        fields = ('username', 'phone', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        validators=(phone_validator,)
    )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('phone', 'password')
