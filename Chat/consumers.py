import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from Authentication.models import User
from .models import ChatRoom, Message 

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_email = text_data_json['sender']
        print(sender_email)

        try:
            room = await sync_to_async(ChatRoom.objects.get)(id=self.room_id)
        except ChatRoom.DoesNotExist:
            return await self.send(text_data=json.dumps({
                'error': 'Chat room does not exist.'
            }))

        try:
            sender = await sync_to_async(User.objects.get)(email=sender_email)
        except User.DoesNotExist:
            return await self.send(text_data=json.dumps({
                'error': 'Sender does not exist.'
            }))

        # Save the message to the database
        await sync_to_async(Message.objects.create)(
            room=room,
            sender=sender,
            content=message
        )
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_email  # Changed to email or username
            }
        )


    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
