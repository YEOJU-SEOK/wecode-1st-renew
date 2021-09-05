from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from user.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


# User model 을 가져옴
User = get_user_model()

# JWT 사용을 위한 기본 설정
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class SignUpSerializer(serializers.Serializer):
    """
    회원 기본 정보 Serializer
    필요한거 : email, password, nickname
    """
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)
    nickname = serializers.CharField(max_length=15)

    def validate(self, data):
        email = data["email"]
        nickname = data["nickname"]

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("이미 존재하는 이메일 입니다")
        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError("이미 존재하는 닉네임 입니다")
        return data

    # DB 에 회원정보를 등록하기 위해 create 함수를 오버라이딩
    # validated_data 인수는 무결성 검사를 통과한 data 를 갖고 있음
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
        )
        # password 의 경우, set_password 함수를 호출하여 암호화된 값을 DB에 저장
        user.set_password(validated_data['password'])
        user.save()
        return Response(user, status=status.HTTP_201_CREATED)


class SignInSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            return {
                'email': 'None'
            }
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }


# 사용자 정보 추출
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)


