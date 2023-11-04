from rest_framework import serializers
from .models import JobPost, RecruiterProfile, Applicants
from seekerFolder.serializers import ProfileSerializer


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicants
        fields = '__all__'


class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        fields = '__all__'


class JPSerializer(serializers.ModelSerializer):
    allprofile = ProfileSerializer(read_only=True)
    applicants = ApplicantSerializer(many=True, read_only=True)

    class Meta:
        model = JobPost
        fields = '__all__'
