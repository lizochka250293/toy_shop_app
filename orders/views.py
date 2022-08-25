from django.shortcuts import redirect
from django.shortcuts import render

from cart.cart import Cart
from .form import OrderCreateForm, AddPayForm
from .models import OrderItem
from .models import PayStatus


def order_create(request):
    """Создание заказа"""
    cart = Cart(request)
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
                h = OrderItem.objects.filter(order=order.id)
                total = 0
                for i in h:
                    total += i.price * i.quantity
                total_int = int(total)
                if order.paid == '1':
                    PayStatus.objects.create(user=request.user, order_id=order.id, total_price=total_int)
                    return render(request, 'orders/pay_card.html', {'order': order})
                cart.clear()
                return render(request, 'orders/created.html',
                              {'order': order, 'user': current_user})
        else:
            form = OrderCreateForm()
        return render(request, 'orders/create.html',
                      {'cart': cart, 'form': form})

    if not request.user.is_authenticated:
        return redirect('login_view')


def add_pay(request):
    """Выбор оплаты"""
    if request.method == 'POST':
        form = AddPayForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = AddPayForm()

    return render(request, 'orders/pay_card.html', {'form': form})
