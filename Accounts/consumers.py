# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.trainer_id = self.scope["user"].id  # Trainer's user ID
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_notification(self, event):
        message = event['message']
        user_id = event['user_id']  # Get the user's ID from the event data

        if user_id:
            # Send the message to the user's WebSocket channel
            await self.channel_layer.send(f"user_{user_id}", {
                'type': 'send_notification',
                'message': message,
            })
