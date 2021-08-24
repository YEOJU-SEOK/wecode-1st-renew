import json, bcrypt, re, jwt

from django.views import View
from django.http import JsonResponse

from .models import User
from my_settings import SECRET, ALGORITHM

from django.shortcuts import render
from .serializers import SignUpSerializer, SignInSerializer, UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from django.contrib.auth import get_user_model

from django.core import cache
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes

# JWT 사용을 위해 필요
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .models import *


#회원가입
class SingUpViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "계정이 성공적으로 생성되었습니다. 로그인해주세요",
        })


#로그인
class SignInViewSet(generics.GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        print("request", request.data)

        serializer.is_valid(raise_exception=True)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        if serializer.validated_data['member_seq'] == "None":
            return Response({"message": "fail"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data.get('email'),
                "token": user['token']
            }
        )

