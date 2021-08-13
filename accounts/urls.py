from accounts.views import AccountsView, ProductsView
from django.urls import path

urlpatterns = [
    path('', AccountsView.as_view(), name='main'),
    path('products/<int:product_id>/', ProductsView.as_view(), name='products'),
]