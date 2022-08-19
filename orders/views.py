from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from app_toy_shop.models import Product
from cart.cart import Cart
from .form import OrderCreateForm, AddPayForm, OrderListForm
from .models import Order, PayStatus
from .models import OrderItem





def order_create(request):
    cart = Cart(request)
    current_user = request.user
    print(request.user.id)
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
                    total += i.price*i.quantity
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
        print('ok')
        return redirect('login_view')


def add_pay(request):
    if request.method == 'POST':
        form = AddPayForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = AddPayForm()

    return render(request, 'orders/pay_card.html', {'form': form})


def orders_list(request):
    order_list = Order.objects.all()
    return render(request, 'orders/orders_list.html',
                      {'order_list': order_list})


def order_detail(request, pk):
    order_items = OrderItem.objects.filter(order_id=pk)
    order = Order.objects.filter(id=pk)
    product = Product.objects.all()
    if request.method == 'POST':
        form = OrderListForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['order_status'])
            order.update(
                order_status=form.cleaned_data['order_status']
            )
        return redirect('orders:orders_list')

    else:
        form = OrderListForm()
    return render(request, 'orders/order_detail.html', {'order': order_items, 'form': form, 'product': product})

