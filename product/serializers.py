from rest_framework import serializers
from product.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    """
    제품 리스트 호출 serializer
    """
    id = serializers.IntegerField(
        help_text="제품 고유번호"
    )
    alt = serializers.CharField(
        source="product.name",
        help_text="제품명",
    )
    #안되면 SerialzierMethodfield
    product_image = serializers.CharField(
        source="product.product_image.image",
        help_text="제품 이미지",
    )
    article_name = serializers.CharField(
        source="product.package.name",
        help_text="항목명",
    )
