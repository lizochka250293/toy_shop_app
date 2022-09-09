from django.urls import path

from . import views
from .views import contact, delivery, refund

app_name = 'shop'

urlpatterns = [
    path('', views.ProductView.as_view(), name='title'),
    path('filter/', views.FilterProductView.as_view(), name='filter'),
    path('add_rating/', views.AddStarRating.as_view(), name='add_rating'),
    path('search/', views.Search.as_view(), name='search'),
    path('<slug:slug>/', views.ToyDetailView.as_view(), name='toy_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('contact', contact, name='contact'),
    path('delivery', delivery, name='delivery'),
    path('refund', refund, name='refund'),

]
