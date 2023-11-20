from userFolder import models, serializers

from seekerFolder.models import Post, Comments, AllProfile
from seekerFolder.serializers import PostSerializer, CommentsSerializer

from rest_framework import generics
from .models import GetDocuments, LogUserEngagement, LogBook
from .serializers import GetDocuSerializer, LogBookSerializer, LogUE

from django.shortcuts import get_object_or_404
from . import for_emailing
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse


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
