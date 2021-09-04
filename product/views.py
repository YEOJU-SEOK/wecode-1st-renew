import json
from django.views import View
from django.http import JsonResponse

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from menu.models import Category
from product.models import Product
from product.serializers import ProductListSerializer, ProductDetailSerializer


class ProductListAPIView(ListAPIView):
    """
    제품 리스트 호출 api
    """
    permission_classes = [AllowAny, ]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.\
            prefetch_related('productimage_set').\
            prefetch_related('option_set').\
            select_related('sub_category')
        return queryset

    def get(self, request, *args, **kwargs):
        """제품 리스트 카테고리별 정렬"""
        sub = request.GET.get("sub", None)
        queryset = self.get_queryset()
        queryset = queryset.filter(sub_category_id=sub)
        serializer = self.get_serializer(queryset, many=True)

        res = {
            "RESP_DATA": serializer.data,
            "RESP_MESSAGE": "성공"
        }

        return Response(res, status=status.HTTP_200_OK)


class ProductDetailAPIView(ListAPIView):
    """
    특정 제품의 상세정보 호출 API
    """
    permission_classes = [AllowAny, ]
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        queryset = Product.objects. \
            select_related('sub_category').\
            prefetch_related('option_set').\
            prefetch_related('productimage_set')
        return queryset

    def get(self, request, package_id, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(package_id=package_id)

        serializer = self.get_serializer(queryset, many=True)

        res = {
            "RESP_DATA": serializer.data,
            "RESP_MESSAGE": "성공"
        }

        return Response(res, status=status.HTTP_200_OK)