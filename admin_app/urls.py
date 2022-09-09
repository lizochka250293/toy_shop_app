from django.urls import path

from . import views
from .views import ProductAdminView, ToyDetailAdminView, Chats, OrderListView, CreateProduct, OrderDetail, \
    ProductAdminDeleteView

app_name = 'admin_app'

urlpatterns = [
    path('all_product/', ProductAdminView.as_view(), name='all_product'),
    path('product_detail/<slug:slug>/', ToyDetailAdminView.as_view(), name='product_detail'),
    path('product_detail/<int:pk>/delete/', ProductAdminDeleteView.as_view(), name='product_delete'),
    path('add_product/', CreateProduct.as_view(), name='add_product'),
    path('orders_list/', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('chats/', Chats.as_view(), name='chats'),
    path('stocks', views.stocks, name='stocks'),
]
