from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from . import models
from .serializers import PostSerializer


@receiver(post_save, sender=models.Post)
def trigger_new_post(sender, instance, created, **kwargs):

    if created:
        print('changes occurred')
        channel_layer = get_channel_layer()
        group_name = 'broadcast'
        serializer = PostSerializer(instance)
        serialized_data = serializer.data
        event = {
            'type': 'new_post',
            'text': serialized_data
        }

        async_to_sync(channel_layer.group_send)(group_name, event)
