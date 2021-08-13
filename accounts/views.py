from django.shortcuts import render
from django.views import View
from accounts.models import *

# Create your views here.
class AccountsView(View):
    def get(self, request):
        products = Product.objects.all().order_by('date_created')
        return render(request, 'accounts/main.html', {'products':products})


class ProductsView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        comments = product.comment_set.all().order_by('date_created')

        context = {
            'product':product,
            'comments':comments,
        }

        return render(request, 'accounts/products.html', context)