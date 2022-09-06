from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import render, redirect
from transliterate import translit

# Create your views here.
from admin_app.forms import ProductDetailForm, StocksForm, ImageProductForm, ImageProductFormSet
from app_toy_shop.models import Product, Image
from chat.models import ChatDialog
from orders.form import OrderListForm
from orders.models import Order, OrderItem
from user.models import User
from .tasks import send_for_users_phone


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
        images = Image.objects.filter(product_id=product.id)
        images_product = []
        for image in images:
            link = {}
            link['link'] = image.link
            images_product.append(link)
        if request.method == 'POST':
            form = ProductDetailForm(data=request.POST, instance=product)
            form_image = ImageProductFormSet(request.POST, request.FILES, initial=images_product)
            if form.is_valid():
                form.save()
            if form_image.is_valid():
                images.delete()
                product_id = Product.objects.get(name=product.name).id
                for p in form_image:
                    product_image = p.save(commit=False)
                    link = p.cleaned_data.get('link')
                    if link is not None:
                        product_image.product_id = product_id
                        product_image.link = link
                        product_image.save()

            return redirect('admin_app:all_product')
        else:
            form = ProductDetailForm(instance=product)
            images = Image.objects.filter(product_id=product.id)
            images_product = []
            for image in images:
                link = {}
                link['link'] = image.link
                images_product.append(link)
            ImageProductFormSet2 = formset_factory(ImageProductForm, extra=3 - len(images_product))
            form_image = ImageProductFormSet2(initial=images_product)
            return render(request, 'admin_app/product_detail.html',
                          {'product': product, 'form': form, 'form_image': form_image})

    else:
        return redirect('shop:title')


def add_product(request):
    """Добавление продукта"""
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProductDetailForm(request.POST, request.FILES)
            form_image = ImageProductFormSet(request.POST, request.FILES)
            if form.is_valid() and form_image.is_valid():
                product = form.save(commit=False)
                name = form.cleaned_data['name'].lower().replace(' ', '_')
                url = translit(name, language_code='ru', reversed=True)
                product.url = url
                product.save()
                product_id = Product.objects.get(name=form.cleaned_data['name']).id
                for p in form_image:
                    product_image = p.save(commit=False)
                    link = p.cleaned_data.get('link')
                    if link is not None:
                        product_image.product_id = product_id
                        product_image.link = link
                        product_image.save()

            return redirect('admin_app:all_product')
        else:
            form = ProductDetailForm()
            form_image = ImageProductFormSet()
            return render(request, 'admin_app/add_product.html', {'form': form, 'form_image': form_image})


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
    """Активные чаты"""
    chats = ChatDialog.objects.filter(is_active=True)
    return render(request, 'admin_app/chats.html', {'chats': chats})


def stocks(request):
    """Акции"""
    if request.method == 'POST':
        form = StocksForm(request.POST)
        if form.is_valid():
            stock = form.cleaned_data['title']
            phones = User.objects.values('phone')
            phone_list = []
            for phone in phones:
                phone_list.append(phone['phone'])
            send_for_users_phone.delay(phone_list, stock)
            return redirect('admin_app:all_product')
    else:
        form = StocksForm()
        return render(request, 'admin_app/stocks.html', {'form': form})

# def add_product_images(request, pk):
#     """Редактировать изображения товара"""
#     if request.method == 'POST':
#         pass
#
#     else:
#         images = Image.objects.filter(product_id=pk)
#         images_product = []
#         for image in images:
#             link = {}
#             link['link'] = image.link
#             images_product.append(link)
#         form_image = ImageProductFormSet(initial=images_product)
#         print(form_image)
#         return render(request, 'admin_app/product_detail.html', {'form_image': form_image})
