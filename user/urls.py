from django.urls import path

from .views import RegisterUser, logout_user, user_room, user_order_detail, order_cancel
from .views import auth_view, verify_view

app_name = 'user'
urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', auth_view, name='login_view'),
    path('logout/', logout_user, name='logout'),
    path('verify/', verify_view, name='verify_view'),
    path('user/<int:pk>/', user_room, name='user_room'),
    path('user_order/<int:pk>/', user_order_detail, name='user_order_detail'),
    path('order_cancel/<int:pk>/', order_cancel, name='order_cancel'),

]
