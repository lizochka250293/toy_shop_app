from django.shortcuts import render

# Create your views here.

from .form import OrderCreateForm
from .models import Order

from django.shortcuts import render
from .models import OrderItem

from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    current_user = request.user
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request, initial={'user': current_user})
        form['user'].value()
        # form = OrderCreateForm(request.POST)
        if form.is_valid():
            print('ok')
            print(form.cleaned_data)
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
                # очистка корзины
            cart.clear()
            return render(request, 'orders/created.html',
                            {'order': order, 'user': current_user})
    else:
        form = OrderCreateForm(request=request, initial={'user': current_user})
    return render(request, 'orders/create.html',
                    {'cart': cart, 'form': form})
