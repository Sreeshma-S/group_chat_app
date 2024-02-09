import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message, ChatRoom

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom_group_name = 'chat_%s' %self.chatroom_name

        await self.channel_layer.group_add(
            self.chatroom_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chatroom_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        chatroom = data['chatroom']

        await self.save_message(username, chatroom, message)

        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chatroom': chatroom,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chatroom = event['chatroom']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chatroom': chatroom,
        }))

    @sync_to_async
    def save_message(self, username, chatroom, message):
        user = User.objects.get(username=username)
        chatroom = ChatRoom.objects.get(slug=chatroom)

        Message.objects.create(user=user, chatroom=chatroom, content=message)
