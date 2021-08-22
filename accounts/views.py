from django import urls
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from accounts.models import *
from accounts.forms import AccountForm, RegisterForm, CommentForm, ProductForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

# Create your views here.
# Models views
# Main page
class LogedInMixin(LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if request.POST.get('logout', '0') == '1':
                logout(request)
                return self.handle_no_permission()
        else:
            return super().dispatch(request, *args, **kwargs)


class AccountsView(LogedInMixin, View):    
    def get(self, request):
        products = Product.objects.all().order_by('date_created')
        return render(request, 'accounts/main.html', {'products':products})


# Product view
class ProductsView(LogedInMixin, View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        comments = product.comment_set.all().order_by('date_created')

        comment_form = CommentForm()

        context = {
            'product':product,
            'comments':comments,
            'comment_form':comment_form,
        }

        return render(request, 'accounts/products.html', context)

    def post(self, request: HttpRequest, product_id):
        remove_product = request.POST.get('delete_product', None)
        comment_to_remove = request.POST.get('delete_comment', None)
        
        if remove_product == str(product_id):
            product = Product.objects.get(id=product_id)
            product.delete()

            return redirect(urls.reverse('main'))

        elif comment_to_remove is None:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.instance
                comment.product = Product.objects.get(id=product_id)
                comment.account = Account.objects.get(id=request.user.account.id)
                comment.save()

        else:
            comment = Comment.objects.get(id=comment_to_remove)
            if (request.user.account.id == comment.account.id):
                comment.delete()

        return self.get(request, product_id)


class UpdateProductCommentView(LogedInMixin, View):
    def get(self, request, product_id, comment_id):
        comment = Comment.objects.get(id=comment_id)
        comment_form = CommentForm(instance=comment)

        context = {
            'comment_form':comment_form
        }

        return render(request, 'accounts/update_product_comment.html', context)

    def post(self, request, product_id, comment_id):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment.objects.get(id=comment_id)
            comment.comment = comment_form.instance.comment
            comment.save()
            return redirect(urls.reverse('products', args=[product_id]))
        else:
            return self.get(request, product_id, comment_id)


# Add & Update product
class AddProductView(LogedInMixin, View):
    def get(self, request):
        form = ProductForm()

        context = {
            'product_form':form
        }

        return render(request, 'accounts/add_product.html', context)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user.account
            form.save()
            return redirect(urls.reverse('main'))
        else:
            return self.get(request)


class UpdateProductView(LogedInMixin, View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = ProductForm(instance=product)

        context = {
            'product_form':form,
        }
        
        return render(request, 'accounts/update_product.html', context)

    def post(self, request, product_id):
        form = ProductForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(id=product_id)
            product.name = form.instance.name
            product.description = form.instance.description
            product.save()
            return redirect(urls.reverse('products', args=[product_id]))
        else:
            return self.get(request)


#Profile
class ProfileView(LogedInMixin, View):
    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = AccountForm(instance=request.user.account)

        context = {
            'profile_form':profile_form,
            'user_form':user_form
        }

        return render(request, 'accounts/profile.html', context)

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = AccountForm(request.POST, request.FILES, instance=request.user.account)

        if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

        return self.get(request)


#Authentication
class NotLogedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(urls.reverse('main'))
        return super().dispatch(request, *args, **kwargs)


class LoginView(NotLogedMixin, View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request: HttpRequest):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user == None:
            respond = render(request, 'accounts/login.html')
        else:
            login(request, user)
            url = request.GET.get('next', urls.reverse('main'))
            respond = redirect(url)

        return respond


class RegisterView(NotLogedMixin, View):
    def get(self, request):
        form = RegisterForm()

        context = {
            'register_form':form
        }

        return render(request, 'accounts/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            respond = redirect(urls.reverse('main'))
        else:
            context = {
                'register_form':form
            }
            respond = render(request, 'accounts/register.html', context)

        return respond


#models API: RESERVED
class ProductsAPI(View):
    def get(self, request):
        products = Product.objects.all()
        return HttpResponse(products)


class CommentsAPI(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        comments = product.comment_set.all().order_by('date_created')
        return HttpResponse(comments)