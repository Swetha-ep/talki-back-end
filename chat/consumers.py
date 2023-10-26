import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message
from Accounts.models import *
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        request_id = self.scope["url_route"]["kwargs"]["id"]
        
        self.room_name = (
            request_id
        )
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await super().disconnect(close_code)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        sender = data["sender"]
        await self.save_message(
            sender=sender, message=message, thread_name=self.room_group_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": sender,
                }
            )
        )
    
    @database_sync_to_async
    def get_user(self, user_id):
        return get_user_model().objects.filter(id=user_id).first()
    

    @database_sync_to_async
    def save_message(self, sender, message, thread_name):
        Message.objects.create(message=message,sender=sender, thread_name=thread_name)