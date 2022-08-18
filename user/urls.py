from django.urls import path

from .views import RegisterUser, LoginUser, logout_user
from .views import home_view, auth_view, verify_view
urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', auth_view, name='login_view'),
    path('logout/', logout_user, name='logout'),
    path('verify/', verify_view, name='verify_view'),

]
