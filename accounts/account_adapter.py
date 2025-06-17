# accounts/account_adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import uuid


class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True

    def clean_username(self, username):
        return str(uuid.uuid4())

from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    print("✅ CustomSocialAccountAdapter loaded")
    def pre_social_login(self, request, sociallogin):
        # Auto-connect social accounts to existing users by email
        email_address = sociallogin.account.extra_data.get("email")

        if not sociallogin.is_existing and email_address:
            try:
                user = User.objects.get(email=email_address)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass  # Will go through the signup flow if no match

    def is_open_for_signup(self, request):
        return True

    def clean_username(self, username):
        return str(uuid.uuid4())

    def send_welcome_email(user):
        print("🚀 CustomSocialAccountAdapter: send_welcome_email triggered")
        subject = "🎉 Welcome to Foxxe Labs!"
        message = render_to_string("emails/welcome_email.txt", {"user": user})
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        self.send_welcome_email(user)
        return user