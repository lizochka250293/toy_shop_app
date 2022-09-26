from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from app_toy_shop.models import Product
from cart.cart import Cart
from .form import OrderCreateForm, AddPayForm
from .models import OrderItem
from .models import PayStatus

# не понимаю как переопределить url если оплата картой
class OrderCreate(FormView, ListView):
    model = Product
    template_name = 'orders/create.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('orders:order_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderCreateForm()
        return context

    def get(self, request, *args, **kwargs):
        self.cart = Cart(request)
        for i in self.cart:
            cur_product = Product.objects.get(id=i['product'].id).quantity
            if cur_product <= i['quantity']:
                info = 'Некоторые товары в Вашей корзине отсутвуют оформление не возможно'
                return render(request, 'orders/create.html', {'info': info})
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.cart = Cart(request)
        if not request.user.is_authenticated:
            return redirect('user:login_view')
        for item in self.cart:
            product = Product.objects.get(id=item['product'].id)
            try:
                total_quantity = product.quantity - item['quantity']
                product.quantity = total_quantity
                product.save()
            except:
                info = 'Некоторые товары в Вашей корзине отсутвуют оформление не возможно'
                return render(request, 'orders/create.html', {'info': info})
        form = self.get_form()
        return self.form_valid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        for item in self.cart:
            OrderItem.objects.create(order_id=self.object.id,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        self.cart.clear()
        if form.cleaned_data['paid'] == '1':
            return redirect('orders:add_pay')
        return HttpResponseRedirect(self.get_success_url())


def order_created(request):
    return render(request, 'orders/created.html')


def order_create(request):
    """Создание заказа"""
    cart = Cart(request)
    for i in cart:
        cur_product = Product.objects.get(id=i['product'].id).quantity
        if cur_product >= i['quantity']:
            current_user = request.user
            if request.user.is_authenticated:
                if request.method == 'POST':
                    form = OrderCreateForm(request.POST)
                    if form.is_valid():
                        order = form.save(commit=False)
                        order.user = request.user
                        order.save()
                        for item in cart:
                            OrderItem.objects.create(order_id=order.id,
                                                     product=item['product'],
                                                     price=item['price'],
                                                     quantity=item['quantity'])

                        items = OrderItem.objects.filter(order=order.id)
                        for item in items:
                            product = Product.objects.get(id=item.product.id)
                            try:
                                total_quantity = product.quantity - item.quantity
                                product.quantity = total_quantity
                                product.save()
                            except:
                                info = 'Некоторые товары в Вашей корзине отсутвуют оформление не возможно'
                                return render(request, 'orders/create.html', {'cart': cart, 'info': info})
                        total = 0
                        for i in items:
                            total += i.price * i.quantity
                        total_int = int(total)
                        if order.paid == '1':
                            PayStatus.objects.create(user=request.user, order_id=order.id, total_price=total_int)
                            cart.clear()
                            return redirect('orders:add_pay')
                        cart.clear()
                        return render(request, 'orders/created.html',
                                      {'order': order, 'user': current_user})
                else:
                    form = OrderCreateForm()
                    return render(request, 'orders/create.html', {'cart': cart, 'form': form})
            if not request.user.is_authenticated:
                return redirect('user:login_view')
        else:
            info = 'Некоторые товары в Вашей корзине отсутвуют оформление не возможно'
            return render(request, 'orders/create.html', {'cart': cart, 'info': info})


def add_pay(request):
    """Выбор оплаты"""
    if request.method == 'POST':
        form = AddPayForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = AddPayForm()

    return render(request, 'orders/pay_card.html', {'form': form})
