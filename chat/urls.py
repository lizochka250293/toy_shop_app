from django.urls import path

from . import views
app_name = 'chat'

urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
    path('chat_close/<str:cur_dialog>/', views.chat_close, name='chat_close')
]
