from asyncio import events
from concurrent.futures import thread
from django.db.models import Q
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.dispatch import receiver
# from django.contrib.auth.models import User
from accounts.models import User, ThreadModel, MessageModel
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

   
    async def connect(self):
        me = self.scope['user']
        
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = await sync_to_async(User.objects.get)(username=other_username)
        try:
            self.thread_obj = await sync_to_async(ThreadModel.objects.get)(Q(user_id=me.id, receiver_id=other_user.id) | Q(user_id=other_user.id, receiver_id=me.id))
        except ObjectDoesNotExist:
            self.thread_obj = await sync_to_async(ThreadModel.objects.create)(user_id=me.id, receiver_id=other_user.id)
        self.room_name = f"personal_thread_{self.thread_obj.id}"
        # self.room_group_name = 'chat_%s' % self.room_name 

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

     
    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )  

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        message = text_data_json['message']
        user_username = text_data_json['user_username']
        # self.command[text_data_json['command']](self, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_username': user_username,
            }
        )
        
        await self.store_message(message)
        print('message:', message)
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_username = event['user_username']
       

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_username': user_username,
        })) 
    @database_sync_to_async
    def store_message(self, message):
        
        MessageModel.objects.create(
            thread = self.thread_obj,
            sender_user_id = self.scope['user'].id,
            # receiver_user = self.other_user,
            body = message
        )
   
    pass
    