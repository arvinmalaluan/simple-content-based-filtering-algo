from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db import transaction
from django.shortcuts import get_object_or_404

from . import models
from . import serializers
from .models import AllProfile


class Messages(generics.ListCreateAPIView):
    queryset = models.Messages.objects.all()
    serializer_class = serializers.Messages


class Conversation(generics.ListCreateAPIView):
    queryset = models.Conversation.objects.all()
    serializer_class = serializers.Conversation


class ConversationUpdate(generics.RetrieveUpdateAPIView):
    queryset = models.Conversation.objects.all()
    serializer_class = serializers.Conversation

    def get_object(self):
        custom_key = self.kwargs['custom_key']
        return get_object_or_404(models.Conversation, custom_key=custom_key)


@api_view(['POST'])
@transaction.atomic
def create_new_message(request):
    sender = AllProfile.objects.get(account=request.data['sender'])
    receiver = AllProfile.objects.get(account=request.data['receiver'])

    return_message = ''

    try:
        # Create a new object in Model1
        obj1 = models.Conversation(
            involve_one=sender, involve_two=receiver)
        obj1.save()

        # Create a new object in Model2
        custom_key = models.Conversation.objects.get(
            custom_key=request.data['custom_key'])
        message = request.data['message']

        obj2 = models.Messages(conversation=custom_key,
                               receiver=request.data['receiver'], message=message)
        obj2.save()

        # Set return value
        return_message = {
            'success': 1, 'message': 'Created successfully', 'custom_key': obj1.custom_key}

    except Exception as e:
        # An error occurred, so we'll roll back the transaction
        transaction.set_rollback(True)
        return_message = {'success': 0, 'message': str(e)}

    return Response(return_message)
