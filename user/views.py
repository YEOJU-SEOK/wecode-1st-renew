from .models import User

from .serializers import SignUpSerializer, SignInSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from rest_framework.response import Response
from rest_framework import status


# JWT 사용을 위해 필요
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .models import *


#회원가입
class SingUpViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "email": request.data["email"],
            "message": "계정이 성공적으로 생성되었습니다. 로그인해주세요",
        })


#로그인
class SignInViewSet(APIView):
    serializer_class = SignInSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['email'] == "None":
            return Response({'message': 'fail'}, status=status.HTTP_200_OK)

        response = {
            "TOKEN": serializer.data["token"],
            "RESP_MESSAGE": "성공"
        }

        return Response(response, status=status.HTTP_200_OK)

