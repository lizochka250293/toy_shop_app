from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from cart.cart import Cart
from .form import OrderCreateForm
from .models import Order
from .models import OrderItem





def order_create(request):
    cart = Cart(request)
    current_user = request.user
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = OrderCreateForm(request.POST, request=request)
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

    if not request.user.is_authenticated:
        print('ok')
        return redirect('login_view')

