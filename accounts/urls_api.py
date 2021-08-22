from accounts.views import ProductsAPI, CommentsAPI
from django.urls import path

urlpatterns = [
    path('products/', ProductsAPI.as_view(), name='get_products'),
    path('products/<int:product_id>/comments/', CommentsAPI.as_view(), name='get_product_comments'),
]