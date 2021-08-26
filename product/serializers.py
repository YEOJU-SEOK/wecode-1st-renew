from rest_framework import serializers
from product.models import Product, Option


class ProductListSerializer(serializers.Serializer):
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
    brand_name = serializers.CharField(
        source="product.brand.name",
        help_text="브랜드 명",
    )
    ispackage = True
    item_badge = serializers.CharField(
        source="product.sale.name",
        help_text="제품 세일주제"
    )
    options = serializers.SerializerMethodField(
        help_text="옵션"
    )

    def get_options(self, obj):
        try:
            options = Option.objects.filter(prduct=obj.products)
            return options
        except AttributeError:
            return ""
