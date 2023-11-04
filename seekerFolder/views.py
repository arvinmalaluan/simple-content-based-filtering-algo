from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.db.models import Prefetch
from rest_framework.response import Response

from .models import Post, Comments, Engagement, Resume, AllProfile
from .serializers import PostSerializer, CommentsSerializer, EngagementSerializer, ResumeSerializer, ProfileSerializer, PostDetailsSerializer, AccWithProfSerializer, CreatePostSerializer
from userFolder import models

from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.http import JsonResponse

from userFolder.models import Account
from chat.models import Messages


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer


class Comment(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class ResumePost(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class ProfilePost(generics.ListCreateAPIView):
    queryset = AllProfile.objects.all()
    serializer_class = ProfileSerializer


class ResumePut(generics.RetrieveUpdateAPIView):
    serializer_class = ResumeSerializer

    def get_object(self):
        account = self.kwargs['account']
        return get_object_or_404(Resume, account=account)


class ProfilePut(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        account = self.kwargs['account']
        return get_object_or_404(AllProfile, account=account)


class CommentPut(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class EngagementSetter(generics.ListCreateAPIView):
    queryset = Engagement.objects.all()
    serializer_class = EngagementSerializer


class EngagementPut(generics.RetrieveUpdateDestroyAPIView):
    queryset = Engagement.objects.all()
    serializer_class = EngagementSerializer

    def get_object(self):
        custom_key = self.kwargs['custom_key']
        return get_object_or_404(Engagement, custom_key=custom_key)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        post = self.get_object()

        comments = Comments.objects.filter(post=post)
        c_serializer = CommentsSerializer(comments, many=True)
        response.data['comments'] = c_serializer.data

        engagements = Engagement.objects.filter(post=post)
        e_serializer = EngagementSerializer(engagements, many=True)
        response.data['engagement'] = e_serializer.data

        return response


class GetAll(generics.ListCreateAPIView):
    serializer_class = PostDetailsSerializer

    def get_queryset(self):
        return Post.objects.prefetch_related('comments', 'engagements').all()


class PWRoles(generics.ListAPIView):
    queryset = AllProfile.get_profiles_with_role([2])
    serializer_class = ProfileSerializer


class GAUWP(generics.ListAPIView):
    serializer_class = AccWithProfSerializer

    def get_queryset(self):
        return models.Account.objects.filter(role__id__in=[2, 3]).prefetch_related('allprofile')


def get_unique_users_last_three_days(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=3)

    print(end_date, start_date)

    unique_users_per_day = Account.objects.filter(
        created__date__range=[start_date, end_date],
        role__in=[2, 3]
    ).annotate(
        activity_date=TruncDate('created')
    ).values('activity_date').annotate(
        unique_user_count=Count('id', distinct=True)
    ).order_by('activity_date')

    pending = Account.objects.filter(
        created__date__range=[start_date, end_date],
        role=3,
        status='pending'
    ).annotate(
        activity_date=TruncDate('created')
    ).values('activity_date').annotate(
        unique_user_count=Count('id', distinct=True)
    ).order_by('activity_date')

    messages = Messages.objects.filter(
        message_created__date__range=[start_date, end_date],
        receiver='18'
    ).annotate(
        activity_date=TruncDate('message_created')
    ).values('activity_date').annotate(
        unique_user_count=Count('conversation', distinct=True)
    ).order_by('activity_date')

    total_users = Account.objects.filter(
        role__in=[2, 3]
    ).aggregate(
        total_count=Count('id', distinct=True)
    )

    total_pending = Account.objects.filter(
        role="3",
        status="pending"
    ).aggregate(
        total_count=Count('id', distinct=True)
    )

    total_messages = Messages.objects.filter(
        receiver="18"
    ).aggregate(
        total_count=Count('conversation', distinct=True)
    )

    users = list(unique_users_per_day)
    pndng = list(pending)
    mssgs = list(messages)

    ttl_users = total_users['total_count']
    ttl_pndng = total_pending['total_count']
    ttl_mssgs = total_messages['total_count']

    print(ttl_users, ttl_pndng, ttl_mssgs)

    data = {'users': users, "pending": pndng, "messages": mssgs,
            'tu': ttl_users, 'tp': ttl_pndng, 'tm': ttl_mssgs}
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_post_with_profiles(request):
    posts = Post.objects.select_related('profile')
    return Response({'success': 1, "token": "hello"})
