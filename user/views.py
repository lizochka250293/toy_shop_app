from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app_toy_shop.models import Product
from orders.models import Order, OrderItem
from .forms import RegisterUserForm, LoginUserForm
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from codes.forms import CodeForm
from user.models import User


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('login_view')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "user/login.html"

    def get_success_url(self):
        return reverse_lazy('title')


def logout_user(request):
    logout(request)
    return redirect('/')


@login_required
def home_view(request):
    return render(request, 'temp/main.html', {})


def auth_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk'] = user.pk
            return redirect('user:verify_view')
    return render(request, 'temp/auth.html', {'form': form})


def verify_view(request):
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

@login_required
def user_room(request, pk):
    if request.user.id == pk:
        orders = Order.objects.filter(user_id=pk)
        return render(request, 'user/user_room.html', {'orders': orders, 'user_id': request.user.id})
    else:
        return redirect('user:login_view')

@login_required
def user_order_detail(request, pk):
    order_items = OrderItem.objects.filter(order_id=pk)
    order = Order.objects.filter(id=pk)
    product = Product.objects.all()
    if request.method == 'POST':
        print('ok')
        order.delete()
        return redirect('user:user_room')
    else:
        return render(request, 'user/user_order_detail.html', {'order': order_items, 'product': product})
