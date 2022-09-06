from django.shortcuts import redirect
from django.shortcuts import render

from app_toy_shop.models import Product
from cart.cart import Cart
from .form import OrderCreateForm, AddPayForm
from .models import OrderItem
from .models import PayStatus



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
