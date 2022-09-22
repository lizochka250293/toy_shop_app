from django.urls import path

from . import views
from .views import OrderCreate

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreate.as_view(), name='order_create'),
    path('add_pay/', views.add_pay, name='add_pay'),
]
