from rest_framework import serializers
from accounts.models import Comment, Account, Product


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Account
        fields = ['url', 'id', 'user', 'profile_picture']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    #author = serializers.ReadOnlyField(source='author.user.username')

    class Meta:
        model = Product
        fields = ['url', 'id', 'name', 'description', 'author', 'date_created']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    #account = serializers.ReadOnlyField(source='account.user.username')
    #product = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Comment
        fields = ['url', 'id', 'product', 'account', 'comment', 'date_created']