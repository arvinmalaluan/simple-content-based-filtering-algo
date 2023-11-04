# app/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q

from .models import Conversation, Messages
from . import serializers


class ConvoConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'user_%s' % self.room_name

       # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data['text']['action']

        if action == 'fetch_all':
            try:
                conversation = Conversation.objects.filter(
                    Q(involve_two=self.room_name) | Q(involve_one=self.room_name))
                serializer = serializers.Conversation(conversation, many=True)
                self.send_chat_message(serializer.data)

            except Conversation.DoesNotExist:
                print('error occured')
                pass

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def chat_message(self, event):
        # Receive message from room group
        text = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': text,
        }))

    def new_convo(self, event):
        self.send(text_data=json.dumps({
            'text': event['text'],
        }))


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print('fetch triggered')

        messages = Messages.last_20_messages(data['text']['custom_key'])
        serializer = serializers.Messages(messages, many=True)
        serialized_messages = serializer.data

        self.send_chat_message(serialized_messages)

    def new_message(self, data):
        custom_key = data['text']['conversation']
        receiver = data['text']['receiver']
        message = data['text']['message']

        try:
            conversation = Conversation.objects.get(custom_key=custom_key)
            message = Messages.objects.create(
                conversation=conversation, receiver=receiver, message=message)
            self.send_chat_message(data['text'])
        except Conversation.DoesNotExist:
            # Handle the case where the conversation doesn't exist
            pass

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'chat_%s' % self.room_name

       # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        self.commands[data['text']['command']](self, data)

    def send_chat_message(self, message):
        print(self.room_group_name)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def chat_message(self, event):
        # Receive message from room group
        text = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': text,
        }))
