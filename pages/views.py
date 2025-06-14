from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

from django.shortcuts import render
from django.views import View

class TestTemplateView(View):
    def get(self, request):
        return render(request, 'pages/test.html')
