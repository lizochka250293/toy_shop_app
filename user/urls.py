from django.urls import path

from .views import RegisterUser, LoginUser, logout_user, user_room, user_order_detail
from .views import home_view, auth_view, verify_view

app_name = 'user'
urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', auth_view, name='login_view'),
    path('logout/', logout_user, name='logout'),
    path('verify/', verify_view, name='verify_view'),
    path('user/<int:pk>/', user_room, name='user_room'),
    path('user_order/<int:pk>/', user_order_detail, name='user_order_detail'),

]
