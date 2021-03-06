import json

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.views import View
from django.http import JsonResponse

from .models import Cart
from user.models import User
from product.models import Product, OptionColor, Option
from user.utils import login_decorator

from .serializers import ShoppingCartSerializer


#generic작성후 viewset으로 전체 구현해보기..
class ShoppingCartAPIView(CreateAPIView, ListAPIView):
    """
    장바구니 등록 & 항목 호출 API
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingCartSerializer
    #post만해서 그냥 갯수 변경하는경우? 에러뜰까 그냥 create될까? -> post작성다 한뒤에 한번 테스트해보기!

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)


class CartView(View):
    #장바구니 등록
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        try:   
            if Cart.objects.filter(
                user=user.id, 
                product=data['product_id'], 
                color=data['color_id']).exists():
                item = Cart.objects.get(
                    user=user.id, 
                    product=data['product_id'], 
                    color=data['color_id'],
                    option=data['option_id'])
                item.quantity += int(data['quantity'])
                item.save()
                return JsonResponse({"message":"SUCCESS"}, status=200)      
            Cart.objects.create(
                user     = User(id = user.id),
                product  = Product(id = data['product_id']),
                quantity = int(data['quantity']),
                color    = OptionColor(id = data['color_id']),
                option    = Option(id = data['option_id'])
            )
            return JsonResponse({"message":"SUCCESS"}, status=201)
        
        except KeyError as ex:
            return JsonResponse({"message":"KEY_ERROR_" + str(ex.args[0])}, status=400)

    #장바구니 조회
    @login_decorator
    def get(self, request):
        user = request.user
        try:
            cart_list = [{
                'id'          : item.id,
                'user_id'     : item.user_id,
                'product_id'  : item.product_id,
                'product_name': item.product.name,
                'quantity'    : item.quantity,
                'color'       : item.color.name,
                'option'       : item.option.price,
                'image_url'   : item.product.information_image
            } for item in Cart.objects.filter(user=user.id)]
            return JsonResponse({"message":"SUCCESS", "CART_LIST": cart_list}, status=200)
        
        except KeyError as ex:
            return JsonResponse({"message":"KEY_ERROR_" + str(ex.args[0])}, status=400)

    #장바구니 갯수변경
class CartDetailView(View):
    @login_decorator
    def patch(self, request, cart_id):
        try: 
            data = json.loads(request.body)
            item = Cart.objects.get(id = cart_id)
            item.quantity = int(data['counts'])
            item.save()
            print()
            return JsonResponse({
                "message"  : "SUCCESS", 
                "QUANTITY" : item.quantity, 
                "PRICE"    : item.option.price * int(item.quantity)}, status=201)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status=400)