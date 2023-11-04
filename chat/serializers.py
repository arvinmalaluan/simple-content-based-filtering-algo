from rest_framework import serializers
from .models import Conversation, Messages
from seekerFolder.serializers import ProfileSerializer


class Conversation(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class ConversationWithProfile(serializers.ModelSerializer):
    involve_one = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = '__all__'


class Messages(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
