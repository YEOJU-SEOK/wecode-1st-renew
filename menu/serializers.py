from rest_framework import serializers
from menu.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    카테고리 리스트 호출 Serializer
    """
    id = serializers.IntegerField(
        help_text="제품 고유번호"
    )
    category = serializers.CharField(
        source="name",
        help_text="카테고리 명")
    sub_category = serializers.SerializerMethodField(
        help_text="하부 카테고리"
    )

    def get_sub_category(self, obj):
        try:
            sub_category = obj.subcategory_set.values('name')
            return sub_category
        except AttributeError:
            return None

    class Meta:
        model = Category
        fields = "__all__"
