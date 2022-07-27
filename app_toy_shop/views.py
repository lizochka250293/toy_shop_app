from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import RegisterUserForm, LoginUserForm, RewiewForm
from .models import Product


class ProductView(ListView):
    #    ***список всех продуктов***
    model = Product
    queryset = Product.objects.filter(is_active=True)
    template_name = 'toy_shop/title.html'

class ToyDetailView(FormMixin, DetailView):
    # один продукт
    model = Product
    slug_field = 'url'
    context_object_name = "toy"
    template_name = 'toy_shop/product_delail.html'
    form_class = RewiewForm

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('toy_delail', kwargs={'slug': slug})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        form = self.get_form()
        return self.form_valid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
# class ToyDetailView(View):
#     def get(self, request, slug):
#         toy = Product.objects.get(url=slug)
#         return render(request, 'toy_shop/product_delail.html', {'toy': toy})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'toy_shop/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('title')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "toy_shop/login.html"

    def get_success_url(self):
        return reverse_lazy('title')

def logout_user(request):
    logout(request)
    return redirect('title')


