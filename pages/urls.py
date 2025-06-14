# pages/urls.py
from django.urls import path

from .views import HomePageView, AboutPageView, TestTemplateView

urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('', HomePageView.as_view(), name='home'),
    path('test/', TestTemplateView.as_view(), name='test_template'),
]
