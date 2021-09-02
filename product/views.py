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
    queryset = Product.objects.\
        prefetch_related('productimage_set').\
        prefetch_related('option_set').\
        select_related('sub_category')
    serializer_class = ProductListSerializer

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
    get_queryset = Product.objects.\
        prefetch_related('productimage_set').\
        prefetch_related('option_set').\
        select_related('sub_category')
    serializer_class = ProductDetailSerializer

    def get(self, request, package_id, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(package_id=package_id)

        serializer = self.get_serializer(queryset, many=True)

        res = {
            "RESP_DATA": serializer.data,
            "RESP_MESSAGE": "성공"
        }

        return Response(res, status=status.HTTP_200_OK)

# class ProductDetailView(View):
#     def get(self, request, package_id):
#         try:
#             products = Product.objects.prefetch_related(
#             'productimage_set',
#             'option_set').select_related(
#             'sub_category').filter(
#             package_id=package_id)
#             context = [{
#                 'id'           : product.id,
#                 'productName'  : product.name,
#                 'product_image': [image.url for image in product.productimage_set.all()],
#                 'brandName'    : product.brand.name,
#                 'articleName'  : product.package.name,
#                 'alt'          : product.package.name,
#                 'sub_category' : product.sub_category.name,
#                 'options'      : [{'color_id':option.option_color.id,'option_id':option.id,'color':option.option_color.name,'price':int(option.price)
#                                 } for option in product.option_set.all()],
#                 'ispackage'    : "true",
#                 'itemBadge'    : product.sale.name,
#                 'infoImage'    : product.information_image,
#                 'category'     : Category.objects.get(id=1).name
#             }for product in products]
#             return JsonResponse({'productdetail' :context}, status=200)
#         except Product.DoesNotExist:
#              return JsonResponse({'MESSAGE':'NO_PRODUCT'}, status=404)
#         except ValueError:
#             return JsonResponse({'message':'VALUE_ERROR'}, status=400)
#
