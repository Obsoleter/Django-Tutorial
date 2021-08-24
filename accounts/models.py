from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    profile_picture = models.ImageField(upload_to='users', null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_account(sender, instance, created, *args, **kwargs):
    if created:
        Account.objects.create(user=instance)


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
        return f"[{self.product.author.user.username}]{self.product.name}: {self.account.user.username}"