from django.contrib import admin

# Register your models here.

from accounts.models import Account, Product, Comment

admin.site.register(Account)
admin.site.register(Product)
admin.site.register(Comment)