from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Account, Comment, Product


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['user']