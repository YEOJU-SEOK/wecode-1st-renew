from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from menu.models import Category
from menu.serializers import CategorySerializer


class CategoryAPiView(ListAPIView):
    """
    카테고리 리스트 호출 APIView
    """
    permission_classes = [AllowAny, ]
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwarg):
        queryset = Category.objects.prefetch_related('subcategory_set').all()
        serializer = self.serializer_class(queryset, many=True)

        res = {
            "RESP_DATA": serializer.data,
            "RESP_MESSAGE": "성공"
        }

        return Response(res, status=status.HTTP_200_OK)
