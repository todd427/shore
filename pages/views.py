from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

from django.shortcuts import render
from django.views import View

class TestTemplateView(View):
    def get(self, request):
        return render(request, 'pages/test.html')
