from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from transliterate import translit

# Create your views here.
from admin_app.forms import ProductDetailForm
from app_toy_shop.models import Product
from chat.models import ChatDialog
from orders.form import OrderListForm
from orders.models import Order, OrderItem


def all_product(request):
    """Вывод всех продуктов для администратора"""
    if request.user.is_superuser:
        products = Product.objects.all()
        return render(request, 'admin_app/all_product.html', {'products': products})
    else:
        return redirect('shop:title')


def product_detail(request, pk):
    """Детали продуктов для администратора"""
    if request.user.is_superuser:
        product = Product.objects.get(id=pk)
        if request.method == 'POST':
            form = ProductDetailForm(request.POST, initial={'name': product.name,
                                                            'description': product.description,
                                                            'price': product.price,
                                                            'poster': product.poster,
                                                            'category': product.category,
                                                            'quantity': product.quantity,
                                                            'is_active': product.is_active})
            if form.is_valid():
                product.name = form.cleaned_data['name']
                product.description = form.cleaned_data['description']
                product.price = form.cleaned_data['price']
                product.poster = form.cleaned_data['poster']
                product.category = form.cleaned_data['category']
                product.quantity = form.cleaned_data['quantity']
                product.is_active = form.cleaned_data['is_active']
                product.save()
            return redirect('admin_app:all_product')
        else:
            form = ProductDetailForm(initial={'name': product.name,
                                              'description': product.description,
                                              'price': product.price,
                                              'poster': product.poster,
                                              'category': product.category,
                                              'quantity': product.quantity,
                                              'is_active': product.is_active})
            return render(request, 'admin_app/product_detail.html', {'product': product, 'form': form})

    else:
        return redirect('shop:title')


def add_product(request):
    """Добавление продукта"""
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProductDetailForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                name = form.cleaned_data['name'].lower().replace(' ', '_')
                url = translit(name, language_code='ru', reversed=True)
                product.url = url
                product.save()
            return redirect('admin_app:all_product')
        else:
            form = ProductDetailForm()
            return render(request, 'admin_app/add_product.html', {'form': form})


@login_required
def orders_list(request):
    """Все заказы для администратора"""
    if request.user.is_superuser:
        order_list = Order.objects.all()
        return render(request, 'admin_app/orders_list.html',
                      {'order_list': order_list})
    else:
        return redirect('shop:title')


@login_required
def order_detail(request, pk):
    """Детали заказа"""
    if request.user.is_superuser:
        order_items = OrderItem.objects.filter(order_id=pk)
        order = Order.objects.get(id=pk)
        product = Product.objects.all()
        if request.method == 'POST':
            form = OrderListForm(request.POST, initial={'order_status': order.order_status})
            if form.is_valid():
                order.order_status = form.cleaned_data['order_status']
                order.save()
            return redirect('admin_app:orders_list')
        else:
            form = OrderListForm(initial={'order_status': order.order_status})
        return render(request, 'admin_app/order_detail.html', {'order': order_items, 'form': form, 'product': product})
    else:
        return redirect('shop:title')


@login_required
def product_delete(request, pk):
    """Удаление продукта"""
    if request.user.is_superuser:
        product = Product.objects.get(id=pk)
        product.delete()
        return redirect('admin_app:all_product')
    else:
        return redirect('shop:title')


def chats(request):
    chats = ChatDialog.objects.filter(is_active=True)
    print(chats)
    return render(request, 'admin_app/chats.html', {'chats': chats})
