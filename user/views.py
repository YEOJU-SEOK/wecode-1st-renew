import json, bcrypt, re, jwt

from django.views import View
from django.http import JsonResponse

from .models import User
from my_settings import SECRET, ALGORITHM

from django.shortcuts import render
from .serializers import SignUpSerializer, SignInSerializer
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


class SignInViewSet(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SignInSerializer
    permission_classes = [AllowAny, ]

