from django.urls import path

from .views import RegisterUser, logout_user, LoginUser, UserRoom, \
    UserOrderDetail, OrderCancel
from .views import verify_view

app_name = 'user'
urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login_view'),
    path('logout/', logout_user, name='logout'),
    path('verify/', verify_view, name='verify_view'),
    path('user/<int:pk>/', UserRoom.as_view(), name='user_room'),
    path('user_order/<int:pk>/', UserOrderDetail.as_view(), name='user_order_detail'),
    path('user_order/<int:pk>/delete/', OrderCancel.as_view(), name='product_delete'),

]
