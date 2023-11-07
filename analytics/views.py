from django.shortcuts import render
from .ml_model import provide_recommendation, provide_compatibility
from rest_framework.response import Response
from rest_framework.decorators import api_view

import numpy as np
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from recruiter.models import JobPost, Applicants
from chat.models import Messages


@api_view(['POST'])
def get_recommendations(request):
    uid = request.data['account']
    skills = request.data['skill']
    education = request.data['education_level']
    achievements = request.data['achievements']

    a = skills.split('_+_')
    b = education.split('_+_')
    c = achievements.split('_+_')

    joined = a + b + c

    var = provide_recommendation(joined)
    return Response({"hello": var})


@api_view(['POST'])
def get_compatibility(request):
    title = request.data['job_title']

    skills = request.data['skills']
    education = request.data['education_level']
    achievements = request.data['achievements']

    a = skills.split('_+_')
    b = education.split('_+_')
    c = achievements.split('_+_')

    print(a, b, c)

    # var = provide_compatibility(title, skills)
    return Response({"return_message": 'hello'})


@api_view(['POST'])
def count_my_posts(request):
    user_id = request.data['id']
    day_counts = []

    for i in range(7):
        date = timezone.now() - timedelta(days=i)
        next_date = timezone.now() - timedelta(days=i-1)
        count = JobPost.objects.filter(
            allprofile=user_id, created__range=(date, next_date)).count()
        day_counts.append({
            "date": date.strftime("%Y-%m-%d"),
            "count": count
        })

    # Sort the list by date
    day_counts = sorted(day_counts, key=lambda x: x['date'])

    return Response({"data": day_counts})


@api_view(['POST'])
def count_my_applicants(request):
    user_id = request.data['id']
    job_ids = JobPost.objects.filter(
        allprofile=user_id).values_list('id', flat=True)
    day_counts = []

    for i in range(7):
        date = timezone.now() - timedelta(days=i)
        next_date = timezone.now() - timedelta(days=i-1)
        count = Applicants.objects.filter(
            job__id__in=job_ids, applied__range=(date, next_date)).count()
        day_counts.append({
            "date": date.strftime("%Y-%m-%d"),
            "count": count
        })

    # Sort the list by date
    day_counts = sorted(day_counts, key=lambda x: x['date'])

    return Response({"data": day_counts})


@api_view(['POST'])
def count_my_messages(request):
    user_id = request.data['id']  # Replace with the actual user ID
    end_date = timezone.now()
    start_date = end_date - timedelta(days=6)

    messages_counts = Messages.objects.filter(
        message_created__range=(start_date, end_date),
        receiver=user_id
    ).values('message_created__date').annotate(count=Count('message_created__date')).order_by()

    # Create a dictionary to store dates and their respective counts
    day_counts = [{"date": item['message_created__date'].strftime(
        '%Y-%m-%d'), "count": item['count']} for item in messages_counts]

    # Create a set of existing dates
    existing_dates = {item['date'] for item in day_counts}

    # Fill in missing dates with count 0
    for i in range(7):
        date = (end_date - timedelta(days=i)).date()
        formatted_date = date.strftime('%Y-%m-%d')
        if formatted_date not in existing_dates:
            day_counts.append({"date": formatted_date, "count": 0})

    # Sort the list by date
    day_counts = sorted(day_counts, key=lambda x: x['date'])

    return Response({"data": day_counts})
