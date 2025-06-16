# accounts/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpPageView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpPageView.as_view(), name='signup'),
]
