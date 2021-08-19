from rest_framework import serializers
from user.models import Gender, User, History


class UserSerializer(serializers.ModelSerializer):
    """
    회원 기본 정보 Serializer
    필요한거 : email, password, nickname
    """
    email = serializers.EmailField(

    )


    class Meta:
        model = User
        fields = "__all__"
