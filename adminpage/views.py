from userFolder import models, serializers

from seekerFolder.models import Post, Comments
from seekerFolder.serializers import PostSerializer, CommentsSerializer

from rest_framework import generics
from .models import GetDocuments, TimeToGetCompatibilityScore, RecordProcessToGetReco
from .serializers import GetDocuSerializer, TTCScoreSerializer, RPTGSerializer


# ---> Start
class G_Documents(generics.ListCreateAPIView):
    queryset = GetDocuments.objects.all()
    serializer_class = GetDocuSerializer


class U_Documents(generics.RetrieveUpdateAPIView):
    queryset = GetDocuments.objects.all()
    serializer_class = GetDocuSerializer


class G_TTGC(generics.ListCreateAPIView):
    queryset = TimeToGetCompatibilityScore.objects.all()
    serializer_class = TTCScoreSerializer


class G_RPTG(generics.ListCreateAPIView):
    queryset = RecordProcessToGetReco.objects.all()
    serializer_class = RPTGSerializer


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
