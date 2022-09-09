from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView

from app_toy_shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """Добавление в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = product.quantity
    form = CartAddProductForm(request.POST, count=quantity)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """Удаление товара из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Детали корзины"""
    cart = Cart(request)
    for i in cart:
        product = Product.objects.get(id=i['product'].id)
        form = CartAddProductForm(count=product.quantity)
        return render(request, 'cart/detail.html', {'cart': cart, 'form': form})
    if not cart:
        return render(request, 'cart/detail.html')


def cart_update(request, product_id):
    """Обновление корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data['quantity']
        cart.add(product, quantity=cd, update_quantity=True)
    return redirect('cart:cart_detail')
