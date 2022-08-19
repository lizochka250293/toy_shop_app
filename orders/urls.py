from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('add_pay/', views.add_pay, name='add_pay'),
    path('orders_list/', views.orders_list, name='orders_list'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
]
