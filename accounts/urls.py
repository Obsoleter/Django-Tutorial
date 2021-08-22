from accounts.views import *
from django.urls import path

urlpatterns = [
    path('', AccountsView.as_view(), name='main'),

    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    path('products/<int:product_id>/', ProductsView.as_view(), name='products'),
    path('products/<int:product_id>/update/<int:comment_id>/', UpdateProductCommentView.as_view(), name='update_product_comment'),

    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('products/<int:product_id>/update/', UpdateProductView.as_view(), name='update_product'),

    path('profile/', ProfileView.as_view(), name='profile'),
]