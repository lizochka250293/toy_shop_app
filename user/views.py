# Create your views here.
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView, FormView

from app_toy_shop.models import Product
from codes.forms import CodeForm
from orders.models import Order, OrderItem
from user.models import User
from .forms import RegisterUserForm, OrderUserForm


class RegisterUser(CreateView):
    """Регистрация пользователя"""
    form_class = RegisterUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login_view')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


def logout_user(request):
    """Выход"""
    logout(request)
    return redirect('/')


@login_required
def home_view(request):
    return render(request, 'temp/main.html', {})


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'temp/auth.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        user = form.get_user()
        self.request.session['pk'] = user.id
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('user:verify_view')


# def auth_view(request):
#     """Авторизация"""
#     form = AuthenticationForm()
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             request.session['pk'] = user.pk
#             return redirect('user:verify_view')
#     return render(request, 'temp/auth.html', {'form': form})


def verify_view(request):
    """Проверка кода"""
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        code_user = f'{user.username}: {user.code}'
        if not request.POST:
            print(code_user)
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('/')
            else:
                return redirect('user:login_view')
    return render(request, 'temp/verify.html', {'form': form})


class UserRoom(LoginRequiredMixin, DetailView):
    """Личный кабинет с заказами"""
    model = User
    template_name = 'user/user_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['orders'] = Order.objects.filter(user_id=user.id)
        return context


# @login_required
# def user_room(request, pk):
#     """Личный кабинет с заказами"""
#     if request.user.id == pk:
#         orders = Order.objects.filter(user_id=pk)
#         return render(request, 'user/user_room.html', {'orders': orders, 'user_id': request.user.id})
#     else:
#         return redirect('user:login_view')


class UserOrderDetail(LoginRequiredMixin, ListView):
    """Детали заказа"""
    model = OrderItem
    template_name = 'user/user_order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.all()
        return context


# @login_required
# def user_order_detail(request, pk):
#     """Детали заказа"""
#     order_items = OrderItem.objects.filter(order_id=pk)
#     order = Order.objects.filter(id=pk)
#     product = Product.objects.all()
#     return render(request, 'user/user_order_detail.html', {'order': order_items, 'product': product})


# @login_required
# def order_cancel(request, pk):
#     """Аннулировать заказ"""
#
#     order = Order.objects.get(id=pk)
#     orders = Order.objects.filter(user_id=order.user_id)
#     order.delete()
#     return render(request, 'user/user_room.html', {'orders': orders, 'user_id': request.user.id})


class OrderCancel(LoginRequiredMixin, FormView, UpdateView):
    """Аннулировать заказ"""
    model = Order

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.order_status = '5'
        self.object.save()
        print(self.object.order_status)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('user:user_room', kwargs={'pk': self.request.user.id})


