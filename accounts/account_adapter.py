# accounts/account_adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True

    def clean_username(self, username):
        return ''

from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Auto-connect social accounts to existing users by email
        email_address = sociallogin.account.extra_data.get("email")

        if not sociallogin.is_existing and email_address:
            try:
                user = User.objects.get(email=email_address)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass  # Will go through the signup flow if no match