from rest_framework import serializers
from .models import Post, Comments, Engagement, Resume, AllProfile
from userFolder.models import Account


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engagement
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllProfile
        fields = '__all__'
        # fields = ['name', 'photo', 'bio', 'social_links', 'location', 'portfolio_link', 'educational_attainment']


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)
    engagements = EngagementSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostDetailsSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True, read_only=True)
    engagements = EngagementSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class AccWithProfSerializer(serializers.ModelSerializer):
    allprofile = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = '__all__'
