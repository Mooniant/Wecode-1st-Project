from django.urls import path
from .views      import DetailView, CategoryProductList, AllProducts, SearchProducts
urlpatterns = [
    path('/<int:page>/',AllProducts.as_view()),
    path('/<int:product_id>', DetailView.as_view()),
    path('/list', CategoryProductList.as_view()),
    path('/search', SearchProducts.as_view()),	

]
