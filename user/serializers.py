from rest_framework import serializers
from user.models import Gender, User, History
from django.contrib.auth import get_user_model

# User model 을 가져옴
User = get_user_model()


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
