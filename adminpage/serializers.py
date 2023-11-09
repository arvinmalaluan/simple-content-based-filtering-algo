from rest_framework import serializers
from . import models


class GetDocuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GetDocuments
        fields = '__all__'


class RPTGSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecordProcessToGetReco
        fields = '__all__'


class TTCScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TimeToGetCompatibilityScore
        fields = '__all__'


class LogUE(serializers.ModelSerializer):
    class Meta:
        model = models.LogUserEngagement
        fields = '__all__'
