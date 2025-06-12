# pages/urls.py
from django.urls import path

from .views import HomePageView, TestTemplateView

app_name = "pages"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path('test/', TestTemplateView.as_view(), name='test_template'),
]
