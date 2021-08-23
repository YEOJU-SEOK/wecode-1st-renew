import json, bcrypt, re, jwt

from django.views import View
from django.http import JsonResponse

from .models import User
from my_settings import SECRET, ALGORITHM

from django.shortcuts import render
from .serializers import SignUpSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model


class Signin(View):

    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.all().filter(email=data['email']).exists():
                if bcrypt.checkpw(data['password'].encode('utf-8'),User.objects.get(email=data['email']).password.encode('utf-8')):
                    access_token = jwt.encode({'id':User.objects.get(email=data['email']).id}, SECRET, ALGORITHM).decode('utf-8')
                    image = User.objects.get(email=data['email']).profile_image
                    name = User.objects.get(email=data['email']).nickname
                    return JsonResponse({"message":"SUCCESS", "TOKEN":access_token, "IMAGE":image, "NAME":name}, status=200)

                return JsonResponse({"message":"INVALID_PW"},status=401)
            return JsonResponse({"message":"INVALID_EMAIL"},status=401)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=403)
        except ValueError:
            return JsonResponse({"message":"INVALID_USER"},status=404)


#회원가입
class SingUpViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny, ]