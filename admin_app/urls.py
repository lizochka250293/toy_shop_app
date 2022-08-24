from django.urls import path

from . import views

app_name = 'admin_app'

urlpatterns = [
    path('all_product/', views.all_product, name='all_product'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('orders_list/', views.orders_list, name='orders_list'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
]
