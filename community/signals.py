from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from seekerFolder import models
from seekerFolder.serializers import PostSerializer


@receiver(post_save, sender=models.Post)
def trigger_new_post(sender, instance, created, **kwargs):

    if created:
        channel_layer = get_channel_layer()
        group_name = 'broadcast'
        event = {
            'type': 'new_post',
            'text': PostSerializer(instance)
        }

        async_to_sync(channel_layer.group_send)(group_name, event)
