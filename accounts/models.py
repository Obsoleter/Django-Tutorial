from django.db import models

# Create your models here.


class Account(models.Model):
    nickname = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    author = models.ForeignKey(Account, models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, models.CASCADE)
    account = models.ForeignKey(Account, models.CASCADE)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"[{self.product.author.nickname}]{self.product.name}: {self.account.nickname}"