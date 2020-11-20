import json
import jwt
import bcrypt

from django.views        import View
from django.http         import JsonResponse
from .models             import User, Cart
from Product.models      import Products
from my_settings         import SECRET_KEY
from decorator           import login_decorator


class CartView(View):
    @login_decorator
    def post(self, request): # ADD 기능
        data = json.loads(request.body) # body에서 product_id를 가져와서
        user_id = request.user

        if Cart.objects.filter(user_id=user_id, product_id = data['product_id']).exists():
            cart = Cart.objects.get(user_id=user_id, product_id=data['product_id'])
            cart.quantity += int(data['quantity'])  # 양만 늘리고
            cart.save()
        else:
            cart = Cart.objects.create(user_id = user_id, product_id=data['product_id'], quantity = int(data['quantity'])) # 아예 없는 물건이라면, 생성.
            cart.save()

        return JsonResponse({'cart_list': "success"}, status=200)

    @login_decorator
    def get(self, request): # 상품 리스트 가져오기
        cart_user = request.user # 임시 유저이름.
        # 전체 상품 리스트 뿌리는 코드 =======================================================
        cart = Cart.objects.filter(user_id=cart_user)

        all_item = []
        for cart_item in cart:
            each_item ={
              "cart_id"             : cart_item.id,
              "id"                  : cart_item.product.id,
              "product_name"        : cart_item.product.name,
              "product_price"       : cart_item.product.price,
              "product_sale_price"  : cart_item.product.sale_price,
              "thumbnail"           : cart_item.product.thumbnail,
              "quantity"            : cart_item.quantity
            }
            all_item.append(each_item)
        # # ===================================================================================

        return JsonResponse({'data' : all_item}, status=200)

    @login_decorator
    def delete(self, request, cart_id):
        Cart.objects.get(id = cart_id).delete()
        return JsonResponse({'data' : 'Deleted'}, status = 200)
