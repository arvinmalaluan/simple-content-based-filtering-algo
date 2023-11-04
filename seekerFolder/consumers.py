# app/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q

from django.forms.models import model_to_dict
from seekerFolder import models
from seekerFolder import serializers


class CommunityConsumer(WebsocketConsumer):
    def connect(self):
        print(self.channel_name + ' opened')
        self.room_group_name = 'broadcast'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print(self.channel_name + ' closed')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        if data['text']['action'] == "fetch_all":
            try:
                posts = models.Post.objects.select_related('profile').prefetch_related(
                    'comments', 'engagements')
                serializer = serializers.PostSerializer(posts, many=True)
                data = serializer.data

                self.send_chat_message(data)

            except:
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

    def new_post(self, event):
        self.send(text_data=json.dumps({
            'text': event['text'],
        }))
        # print(event['text'])
