from rest_framework import serializers
from menu.models import Category
from product.models import Product, Option, ProductImage


class ProductListSerializer(serializers.ModelSerializer):
    """
    제품 리스트 호출 serializer
    """
    id = serializers.IntegerField(
        help_text="제품 고유번호"
    )
    alt = serializers.CharField(
        source="name",
        help_text="제품명",
    )
    product_image = serializers.SerializerMethodField(
        help_text="제품 이미지",
    )
    article_name = serializers.CharField(
        source="package.name",
        help_text="항목명",
    )
    brand_name = serializers.CharField(
        source="brand.name",
        help_text="브랜드 명",
    )
    item_badge = serializers.CharField(
        source="sale.name",
        help_text="제품 세일주제"
    )
    options = serializers.SerializerMethodField(
        help_text="옵션"
    )

    def get_options(self, obj):
        try:
            options = obj.option_set.values()
            return options
        except AttributeError:
            return ""

    def get_product_image(self, obj):
        try:
            product_image = obj.productimage_set.values('url')
            return product_image

        except AttributeError:
            return ""

    class Meta:
        model = Product
        fields = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    특정 제품의 상세정보 serializer
    """
    id = serializers.IntegerField(
        help_text="제품 고유번호"
    )
    product_name = serializers.CharField(
        source="name",
        help_text="제품명",
    )
    product_image = serializers.SerializerMethodField(
        help_text="제품 이미지",
    )
    brand_name = serializers.CharField(
        source="brand.name",
        help_text="브랜드 명",
    )
    article_name = serializers.CharField(
        source="package.name",
        help_text="항목명",
    )
    brand_name = serializers.CharField(
        source="brand.name",
        help_text="브랜드 명",
    )
    item_badge = serializers.CharField(
        source="sale.name",
        help_text="제품 세일주제"
    )
    alt = serializers.CharField(
        source="name",
        help_text="제품명",
    )
    sub_category = serializers.CharField(
        source="sub_category.name",
        help_text="카테고리명",
    )
    options = serializers.SerializerMethodField(
        help_text="옵션종류",
    )

    is_package = serializers.SerializerMethodField(
        help_text="묶음여부"

    )
    item_badge = serializers.CharField(
        source="sale.name",
        help_text="제품 세일주제"
    )
    info_image = serializers.CharField(
        source="information_image",
        help_text="제품 세일주제"
    )
    category = serializers.SerializerMethodField(
        help_text="카테고리명",
    )

    def get_options(self, obj):
        try:
            options = obj.option_set.values()
            return options
        except AttributeError:
            return ""

    def get_product_image(self, obj):
        try:
            product_image = obj.productimage_set.values('url')
            return product_image

        except AttributeError:
            return ""

    def get_is_package(self, obj):
        return True

    def get_category(self, obj):
        try:
            category = Category.objects.get(id=1).name

            return category

        except AttributeError:
            return ""

    class Meta:
        model = Product
        fields = "__all__"
