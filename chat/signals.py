from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.forms.models import model_to_dict

from . import models
from . import serializers


@receiver(post_save, sender=models.Conversation)
def trigger_new_convo(sender, created, instance, **kwargs):
    item = model_to_dict(instance)

    if created:
        print('changes occurred')
        channel_layer = get_channel_layer()
        channel_sender = "user_" + str(item['involve_one'])
        channel_receiver = "user_" + str(item['involve_two'])
        serializer = serializers.Conversation(instance)
        serialized_data = serializer.data
        event = {
            'type': 'new_convo',
            'text': serialized_data
        }

        async_to_sync(channel_layer.group_send)(channel_sender, event)
        async_to_sync(channel_layer.group_send)(channel_receiver, event)
