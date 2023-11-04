from .serializers import *
from .models import Account

import jwt
import secrets

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.hashers import check_password


def create_token(data):

    refresh = RefreshToken.for_user(data)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return {'access': access_token, 'refresh': refresh_token}


@api_view(['POST'])
def login(request):
    user = get_object_or_404(Account, Q(username=request.data['identifier']) | Q(
        email=request.data['identifier']))

    # validate whether the raw password or the password input is the same with the hashed password or the saved password
    does_match = check_password(request.data['password'], user.password)
    print(does_match)

    if does_match:
        user = Account.objects.get(Q(email=request.data['identifier']) | Q(
            username=request.data['identifier']))

        # token = create_token(user)
        payload = {
            "user_id": user.id,
            "user_email": user.email,
            "user_username": user.username,
            "user_role": user.role.id
        }

        secret_key = secrets.token_hex(32)
        token = jwt.encode(payload, secret_key)

        return Response({'success': 1, "token": token})

    return Response({'success': 0, 'message': 'invalid log in credential'})


@api_view(['POST'])
def register(request):
    serializer = UserAccountSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'success': 1})

    return Response({'success': 0, 'message': serializer.errors})


@api_view(['POST'])
def get_user_info(request):
    account = Account.objects.get(id=request.data['id'])
    serializer = UserAccountSerializer(account)

    return Response({'data': serializer.data})


class getAccount(generics.RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = UserAccountSerializer


@api_view(['GET'])
def get_all_info(request):
    account = Account.objects.all()
    serializer = UserAccountSerializer(account, many=True).data

    return Response({'data': serializer})


@api_view(['PUT'])
def update_user_info(request):
    user = get_object_or_404(Account, id=request.data['account'])
    does_match = check_password(request.data['old_password'], user.password)

    try:

        if not does_match:
            return Response({'failed': 'password does not match'})

        account = Account.objects.get(id=request.data['account'])
        serializer = UserAccountSerializer(account, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": 1, "data": serializer.data})

        return Response({'failed': serializer.errors})

    except Account.DoesNotExist:
        return Response({'success': 0, 'message': 'not found'})
