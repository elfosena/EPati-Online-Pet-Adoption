import datetime
import json
from time import timezone
from urllib import response
from channels.consumer import AsyncConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from chat.models import Thread, ChatMessage

User = get_user_model()


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('connected', event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name,
        )
        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):
        print('receive', event)
        recieved_data = json.loads(event['text'])
        msg = recieved_data.get('message')
        sent_by_id = recieved_data.get('sent_by')
        send_to_id = recieved_data.get('send_to')
        thread_id = recieved_data.get('thread_id')

        if not msg:
            return False

        sent_by = await self.get_user_object(sent_by_id)
        send_to = await self.get_user_object(send_to_id)
        thread = await self.get_thread(thread_id)

        await self.create_chat_message(thread, sent_by, msg)

        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']

        response = {
            'message': msg,
            'sent_by': self_user.id,
            'thread_id': thread_id,
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response),
            }
        )        
        
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response),
            }
        )

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })

    @database_sync_to_async
    def get_user_object(self, user_id):
        user = User.objects.filter(id=user_id)

        if user.exists():
            return user.first()
        else:
            return None

    @database_sync_to_async
    def get_thread(self, user_id):
        thread = Thread.objects.filter(id=user_id)

        if thread.exists():
            return thread.first()
        else:
            return None

    @database_sync_to_async
    def create_chat_message(self, thread, sent_by, message):
        if not ChatMessage.objects.filter(thread=thread, user=sent_by, message=message).exists():
            thread.save()
            ChatMessage.objects.create(thread=thread, user=sent_by, message=message)
