from django.db import transaction

from rest_framework import serializers

from .models import Cart
from product.models import Product, OptionColor, Option
from user.models import User


class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    장바구니 등록 & 항목 호출 srializer
    """
    user = serializers.SerializerMethodField(
        help_text="유저"
    )
    product = serializers.SerializerMethodField(
        help_text="상품"
    )
    quantity = serializers.IntegerField(
        help_text="수량"
    )
    color = serializers.SerializerMethodField(
        help_text="컬러"
    )
    option = serializers.SerializerMethodField(
        help_text="옵션")

    def get_user(self, obj):
        return obj.user.id

    def get_product(self, obj):
        #check
        product = Product.objects.get(id=obj.product_id)
        return product

    def get_color(self, obj):
        #check
        color = OptionColor.objects.filter(id=obj.color_id)
        return color

    def get_option(self, obj):
        #check
        option = Option.objects.filter(id=obj.option_id)
        return option

    def validate(self, data):
        #이미 카트에 추가되어있는지 확인
        if Cart.objects.filter(
                user=data.user.id,
                product=data['product_id'],
                color=data['color_id']
        ).exists():
            raise serializers.ValidationError("이미 추가되어있는 제품입니다")

        return data

    @transaction.atomic()
    def create(self, validated_data):
        cart = Cart.objects.create(**validated_data)
        return cart

    class Meta:
        model = Cart
        #원하는 값만 나오는지 체크~
        fields = "__all__"