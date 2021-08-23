from rest_framework import serializers
from user.models import Gender, User, History
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings


# User model 을 가져옴
User = get_user_model()

#JWT사용을 위한 기본 설정
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class SignUpSerializer(serializers.ModelSerializer):
    """
    회원 기본 정보 Serializer
    필요한거 : email, password, nickname
    """

    password = serializers.CharField(write_only=True)

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
        return user

    class Meta:
        model = User
        fields = ["email", "password", "nickname"]


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password", None)

        user = authenticate(email=email, password=password)

        if user is None:
            return {"member_seq": "None", "email": email}
        try:
            payload = JWT_PAYLOAD_HANDLER(user) #payload생성
            jwt_token = JWT_ENCODE_HANDLER(payload) #jwt token 생성

        except User.DoesNotExist:
            raise serializers.ValidationError("이메일 혹은 비밀번호가 존재하지 않습니다")

        return {
            "member_seq": user.member_seq,
            "token": jwt_token
        }


# 사용자 정보 추출
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',)


