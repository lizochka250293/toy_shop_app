import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.http import request

from chat.models import ChatMessage, ChatDialog
from user.models import User

user = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        if text_data_json.get('action') == 'close':
            await self.chat_close(text_data_json.get('chat'))
            return

        message = text_data_json['message']
        username = self.scope["user"]
        print(username, type(username))
        await self.write_message(message, username)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': await self.get_username(username)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    @database_sync_to_async
    def get_username(self, username):
        user = User.objects.get(username=username).username
        print('user', user)
        return user

    @database_sync_to_async
    def write_message(self, message, username):
        dialog = ChatDialog.objects.get(id=self.room_name)
        if not dialog.is_active:
            dialog.is_active = True
            dialog.save()
        print(dialog.is_active)
        ChatMessage.objects.create(dialog_id=dialog.id, body=message, user_id=User.objects.get(username=username).id)

    @database_sync_to_async
    def chat_close(self, dialog):
        dialog_close = ChatDialog.objects.get(id=dialog)
        dialog_close.is_active = False
        dialog_close.save()
