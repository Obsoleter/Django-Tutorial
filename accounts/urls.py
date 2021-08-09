from accounts.views import AccountsView
from django.urls import path

urlpatterns = [
    path('', AccountsView.as_view()),
]