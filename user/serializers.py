from rest_framework import serializers
from user.models import Gender, User, History


class UserSerializer(serializers.ModelSerializer):
    """
    회원 기본 정보 Serializer
    필요한거 : email, password, nickname
    """
    email = serializers.EmailField(
        help_text="회원 고유 번호",
    )
    password = serializers.CharField(
        help_text="비밀번호(수정)"
    )
    nickname = serializers.CharField(
        help_text="닉네임"
    )

    class Meta:
        model = User
        fields = "__all__"
