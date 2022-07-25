from django.shortcuts import render
from django.views import View
from .models import Product


class ProductView(View):
#    ***список всех продуктов***
     def get(self, request):
         products = Product.objects.all()
         return render(request, 'toy_shop/product_all.html', {"product_list":products})
