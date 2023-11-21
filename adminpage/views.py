from userFolder import models, serializers

from seekerFolder.models import Post, Comments, AllProfile
from seekerFolder.serializers import PostSerializer, CommentsSerializer

from rest_framework import generics
from .models import GetDocuments, LogUserEngagement, LogBook
from .serializers import GetDocuSerializer, LogBookSerializer, LogUE
from recruiter.models import Applicants

from django.shortcuts import get_object_or_404
from . import for_emailing
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone


# ---> Start
class G_Documents(generics.ListCreateAPIView):
    queryset = GetDocuments.objects.all()
    serializer_class = GetDocuSerializer


class G_LUE(generics.ListCreateAPIView):
    queryset = LogUserEngagement.objects.all()
    serializer_class = LogUE


class U_Documents(generics.RetrieveUpdateAPIView):
    queryset = GetDocuments.objects.all()
    serializer_class = GetDocuSerializer

    def get_object(self):
        fk_account = self.kwargs['fk_account']
        print(fk_account)
        return get_object_or_404(GetDocuments, fk_account_id=fk_account)


class CreateLogBook(generics.ListCreateAPIView):
    queryset = LogBook.objects.all()
    serializer_class = LogBookSerializer


class UpdateLogBook(generics.RetrieveUpdateAPIView):
    queryset = LogBook.objects.all()
    serializer_class = LogBookSerializer


class G_Accounts(generics.ListCreateAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.UserAccountSerializer


class UD_Accounts(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.UserAccountSerializer


class G_Posts(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UD_Posts(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class G_Comments(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class UD_Comments(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


@api_view(['POST'])
def send_invite(request):
    comp = AllProfile.objects.get(account=request.data['comp_name'])
    name = AllProfile.objects.get(account=request.data['name'])

    content = {
        "comp_name": comp.name,
        "name": name.name,
        "target": name.fk.email
    }

    for_emailing.send_invitations(content)

    return JsonResponse({'success': 1})


@api_view(['POST'])
def lower_stat(request):
    uid = request.data['uid']
    jid = request.data['jid']

    gender_distribution = AllProfile.objects.filter(fk__role__role="seeker").values('gender').annotate(count=Count('gender'))
    new_distribution = list(gender_distribution)  # Convert QuerySet to list

    # Rename 'gender' key to 'name'
    for item in new_distribution:
        item['name'] = item.pop('gender')

    print(new_distribution)

    today = timezone.now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)  # Sunday

    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timezone.timedelta(days=32)
                    ).replace(day=1) - timezone.timedelta(days=1)

    if Applicants.objects.filter(job__allprofile__account=uid).exists():
        ji_today_count = Applicants.objects.filter(
            job__allprofile__account=uid, interview__date=today
        ).count() or 0

        ji_this_week_count = Applicants.objects.filter(
            job__allprofile__account=uid, interview__date__range=[
                start_of_week, end_of_week]
        ).count() or 0

        ji_this_month_count = Applicants.objects.filter(
            job__allprofile__account=uid, interview__date__range=[
                start_of_month, end_of_month]
        ).count() or 0

    return Response({"success": 1, "gender": new_distribution, "sched": [{"name": "today", "count": ji_today_count}, {"name": "this week", "count": ji_this_week_count}, {"name": "this month", "count": ji_this_month_count}]})
