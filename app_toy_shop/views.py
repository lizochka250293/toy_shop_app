from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from cart.forms import CartAddProductForm
from .forms import ReviewForm, RatingForm
from .models import Product, Category, StarForProduct


class GetCategory:
    """Все категории"""

    def get_category(self):
        return Category.objects.all()


class ProductView(GetCategory, ListView):
    """Список всех товаров"""
    model = Product
    queryset = Product.objects.filter(is_active=True)
    template_name = 'toy_shop/title.html'
    paginate_by = 3


class ToyDetailView(GetCategory, FormMixin, DetailView):
    """Вывод одного товара"""
    model = Product
    slug_field = 'url'
    context_object_name = "product"
    template_name = 'toy_shop/product_detail.html'
    form_class = CartAddProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['form'] = CartAddProductForm(count=product.quantity)
        context['star_form'] = RatingForm()
        return context


class FilterProductView(GetCategory, ListView):
    """Добавление фильтра товаров"""
    template_name = 'toy_shop/title.html'

    def get_queryset(self):
        queryset = Product.objects.filter(category__name__in=self.request.GET.getlist('category'))
        return queryset


class Search(ListView):
    """Поиск товаров"""
    template_name = 'toy_shop/title.html'

    def get_queryset(self):
        product = Product.objects.none()
        if self.request.GET.get('q'):
            product = Product.objects.filter(name__icontains=self.request.GET.get('q').capitalize())
        return product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class AddStarRating(View):
    """Добавление рейтинга товара"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        print(int(request.POST.get("star")))
        if form.is_valid():
            print('ok')
            StarForProduct.objects.update_or_create(
                ip=self.get_client_ip(request),
                product_id=int(request.POST.get("product")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class AddReview(View):
    """Добавление отзыва к товару"""

    def post(self, request, pk):
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            product = Product.objects.get(id=pk)
            if form.is_valid():
                form = form.save(commit=False)
                form.product_id = product.id
                form.user_id = request.user.id
                form.save()

            return render(request, 'toy_shop/product_detail.html', {'product': product})
        else:
            return redirect('login_view')

# не правильно построен url
def contanc(request):
    """Контакты"""
    return render(request, 'toy_shop/contact.html')


def delivery(request):
    """Доставка"""
    return render(request, 'toy_shop/delivery.html')


def refund(request):
    """Возрат"""
    return render(request, 'toy_shop/refund.html')
