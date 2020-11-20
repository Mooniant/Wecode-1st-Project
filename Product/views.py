from django.shortcuts      import render
from django.views          import View
from django.http           import JsonResponse
from django.db             import models
from Product.models        import *


class DetailView(View):
    def get(self, request,product_id):
        try:
            detail_product = Products.objects.get(id=product_id)
            product_image = detail_product.detailimageurl_set.all()
            product_related = detail_product.product.all()
            
        except Products.DoesNotExist:
            return JsonResponse({'message' : 'INVALID PRODUCT'}, status=400)

        product_group = Products.objects.filter(product_group_id = detail_product.product_group.id)

        product_info = {
            "name"       : detail_product.name,
            "price"      : detail_product.price,
            "sale_price" : detail_product.sale_price,
            "point"      : detail_product.point,
            "description": detail_product.description,
            "info"       : detail_product.info,
            "notice"     : detail_product.notice,
            "group"      : [each_item.id for each_item in product_group],
            "detailimage": [each_image.detailImage for each_image in product_image],
            "related"    : [each_related.related_product.id for each_related in product_related]
        }
        
        return JsonResponse({'product_name' : product_info}, status=200)


class SearchProducts(View):
    def get(self, request):
        search_key = request.GET.get('keyword', None)

        if search_key != "":
            all_product = Products.objects.filter(name__icontains=search_key)
            product_list =[
                {
                    "product_name" : each_product.name,
                }
            for each_product in all_product]
            return JsonResponse({'list' : product_list}, status=200)
        else :
            return JsonResponse({'message' : 'It doesnt exist'}, status=400)

        
         
class CategoryProductList(View):
    def get(self, request):
        category_id = int(request.GET.get('category', None))
        subcategory_id = int(request.GET.get('subcategory', None))
        order_sort = int(request.GET.get('sorting', None))
        try:
            subcategories = SubCategory.objects.prefetch_related('products_set').filter(category_id=category_id, id = subcategory_id)[0]
        except SubCategory.DoesNotExist:
            return JsonResponse({'message' : 'Sub Does not exist'}, status = 400)

        if order_sort == 0:
            all_product = subcategories.products_set.all().order_by('price')
        elif order_sort == 1:
            all_product = subcategories.products_set.all().order_by('-price')
        product_list = [
            {
                "name"      : each_product.name,
                "thumbnail" : each_product.thumbnail,
                "price"     : each_product.price,
            } for each_product in all_product]

        return JsonResponse({'list' : product_list}, status=200)


class AllProducts(View):
    def get(self,request,page):
        page_limit = int(request.GET.get('limit', None)) # 갯수

        try :
            all_product = Products.objects.filter()[(page-1)*page_limit : page*page_limit]
        except :
            return JsonResponse({'message' : 'INVALID LIST'}, status=400)
        
        product_list = [
            {
                "id"        : each_product.id,
                "name"      : each_product.name,
                "thumbnail" : each_product.thumbnail,
                "price"     : each_product.price,
            } for each_product in all_product]

        return JsonResponse({'list' : product_list}, status = 200)

