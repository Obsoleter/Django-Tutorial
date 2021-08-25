import re
from django.http import Http404

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from api import serializers

from api.serializers import *
from accounts.models import *

# Create your views here.
class IsOwnerOrReadOnly(permissions.BasePermission):
     def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.account == request.user.account

class IsAuthorOrReadOnly(permissions.BasePermission):
     def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user.account


# Product
class ProducViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.account)


# Account
class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['id', 'user']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).get(id=request.user.account.id)

        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


# Comment
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)