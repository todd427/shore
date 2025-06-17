from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import uuid


class NoSignupFormAdapter(DefaultSocialAccountAdapter):
    print("✅ NoSignupFormAdapter loaded")
    def is_open_for_signup(self, request, sociallogin):
        return True

    def is_auto_signup_allowed(self, request, sociallogin):
        user = sociallogin.user
        email = user.email or sociallogin.account.extra_data.get("email")
        return bool(email)

    def send_welcome_email(self, user):
        try:
            print("📨 NoSignupFormAdapter: sending welcome email to", user.email)
            subject = "🎉 Welcome to Foxxe Labs!"
            message = render_to_string("emails/welcome_email.txt", {"user": user})
            #print("📧 Composed message:\n", message)
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print("🔥 Error sending email:", e)

    def save_user(self, request, sociallogin, form=None):
        print("🚀 NoSignupFormAdapter: save_user triggered")
        user = sociallogin.user
        extra_data = sociallogin.account.extra_data

        user.email = user.email or extra_data.get('email')
        user.first_name = user.first_name or extra_data.get('given_name', '')
        user.last_name = user.last_name or extra_data.get('family_name', '')
        user.username = ''
        user.is_active = True
        user.save()

        return user


class CustomAccountAdapter(DefaultAccountAdapter):
    print("✅ CustomAccountAdapter loaded")
    def is_open_for_signup(self, request):
        return True

    def clean_username(self, username):
        return str(uuid.uuid4())

    def send_welcome_email(self, user):
        try:
            print("📨 CustomAccountAdapter: sending welcome email to", user.email)
            subject = "🎉 Welcome to Foxxe Labs!"
            message = render_to_string("emails/welcome_email.txt", {"user": user})
            #print("📧 Composed message:\n", message)
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print("🔥 Error sending email:", e)

    def save_user(self, request, user, form, commit=True):
        print("🚀 CustomAccountAdapter: save_user triggered")
        user = super().save_user(request, user, form, commit)
        self.send_welcome_email(user)
        return user

from django.core.mail import get_connection
from django.conf import settings

try:
    connection = get_connection()
    print("📡 Email connection test:", connection)
    print("📨 Email backend:", settings.EMAIL_BACKEND)
except Exception as e:
    print("❌ Email connection error:", e)
