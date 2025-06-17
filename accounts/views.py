from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.conf import settings

from allauth.account.adapter import get_adapter
print("🧭 Adapter in use:", get_adapter())

def test_email(request):
    user = get_user_model().objects.first()
    if not user:
        return HttpResponse("No user found")

    message = render_to_string("emails/welcome_email.txt", {"user": user})
    send_mail(
        "Test Email from View",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return HttpResponse(f"Sent email to {user.email}")
