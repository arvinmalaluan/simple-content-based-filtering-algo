from rest_framework import serializers
from . import models


class GetDocuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GetDocuments
        fields = '__all__'


class RPTGSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogBook
        fields = '__all__'


class LogUE(serializers.ModelSerializer):
    class Meta:
        model = models.LogUserEngagement
        fields = '__all__'
