from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView
from cart.forms import CartAddProductForm
from .forms import ReviewForm, RatingForm
from .models import Product, Category, StarForProduct


class GetCategory:

    def get_category(self):
        return Category.objects.all()


class ProductView(GetCategory, ListView):
    #    ***список всех продуктов***
    model = Product
    queryset = Product.objects.filter(is_active=True)
    template_name = 'toy_shop/title.html'
    paginate_by = 3


# class ToyDetailView(GetCategory, FormMixin, DetailView):
#     # один продукт
#     model = Product
#     slug_field = 'url'
#     context_object_name = "toy"
#     template_name = 'toy_shop/product_detail.html'
#     form_class = ReviewForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['star_form'] = RatingForm()
#         return context
#
#     def get_success_url(self):
#         slug = self.kwargs['slug']
#         return reverse('toy_detail', kwargs={'slug': slug})
#
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('login')
#         form = self.get_form()
#         return self.form_valid(form)
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.product = self.get_object()
#         self.object.user = self.request.user
#         self.object.save()
#         return super().form_valid(form)
class ToyDetailView(GetCategory, FormMixin, DetailView):
    model = Product
    slug_field = 'url'
    context_object_name = "product"
    template_name = 'toy_shop/product_detail_2.html'
    form_class = CartAddProductForm
# def product_detail(request, slug):
#     product = Product.objects.get(url=slug)
#     cart_product_form = CartAddProductForm()
#     return render(request, 'toy_shop/product_detail_2.html', {'product': product,
#                                                         'cart_product_form': cart_product_form})




class FilterProductView(GetCategory, ListView):
    # фильтр продуктов
    template_name = 'toy_shop/title.html'

    def get_queryset(self):
        queryset = Product.objects.filter(category__name__in=self.request.GET.getlist('category'))
        print(queryset)
        return queryset


class Search(ListView):
    # поиск продуктов
    template_name = 'toy_shop/title.html'

    def get_queryset(self):
        product = Product.objects.none()
        if self.request.GET.get('q'):
            product = Product.objects.filter(name__icontains=self.request.GET.get('q'))
        return product
        # return Product.objects.filter(name__icontains=self.request.GET.get('g'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            StarForProduct.objects.update_or_create(
                ip=self.get_client_ip(request),
                product_id=int(request.POST.get("product")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)



class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            print(form.cleaned_data)
            form = form.save(commit=False)
            form.product_id = product
            print(request.user.id)
            form.user_id = request.user.id
            form.save()

        return redirect('title')


