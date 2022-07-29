from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterUserForm, LoginUserForm
# Create your views here.


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('title')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "user/login.html"

    def get_success_url(self):
        return reverse_lazy('title')


def logout_user(request):
    logout(request)
    return redirect('title')
