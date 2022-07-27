from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import Textarea

from app_toy_shop.models import User, Reviews


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Телефон')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повтор пароля')
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class RewiewForm(forms.ModelForm):
    description = forms.CharField(label='', widget=Textarea(attrs={'rows': 5}))


    class Meta:
        model = Reviews
        fields = ["description"]
