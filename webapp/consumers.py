import json
from channels.generic.websocket import AsyncWebsocketConsumer
from webapp.models import productdb,signupdb,Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.buyer = self.scope['url_route']['kwargs']['buyer']
        self.seller = self.scope['url_route']['kwargs']['seller']
        self.room_name = f"{self.buyer}_{self.seller}"

        # Join the room
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_name = data['sender']
        sender = signupdb.objects.get(Name=sender_name)
        receiver_name = self.seller if sender_name == self.buyer else self.buyer
        receiver = signupdb.objects.get(Name=receiver_name)
        product = productdb.objects.get(Username=self.seller)

        # Save to database
        Message.objects.create(sender=sender, receiver=receiver, product=product, content=message)

        # Broadcast to the group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_name,
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))
