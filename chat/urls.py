from django.urls import path

from . import views
from .views import Room

app_name = 'chat'

urlpatterns = [
    path('<int:room_name>/', Room.as_view(), name='room'),
    # path('chat_close/<str:cur_dialog>/', views.chat_close, name='chat_close')
]
