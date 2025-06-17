from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

class LanderPageView(TemplateView):
    template_name = 'lander.html'

class ContactPageView(TemplateView):
    template_name = 'contact.html'

from django.shortcuts import render
from django.views import View

class TestTemplateView(View):
    def get(self, request):
        return render(request, 'pages/test.html')
    
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def test_email_view(request):
    try:
        send_mail(
            subject="test-email.txt",
            message = render_to_string("emails/test-email.txt"),
            from_email="mork@foxxelabs.com",
            recipient_list=["todd@toddwriter.com"],
            fail_silently=False,
        )
        return HttpResponse(f"✅ Email sent successfully using backend: {settings.EMAIL_BACKEND}")

    except Exception as e:
        return HttpResponse(f"❌ Email failed: {str(e)}", status=500)
