from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter


class NoSignupFormAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        # Always allow social signup
        return True

    def is_auto_signup_allowed(self, request, sociallogin):
        user = sociallogin.user
        email = user.email or sociallogin.account.extra_data.get("email")
        return bool(email)

    def save_user(self, request, sociallogin, form=None):
        # Extract useful fields
        user = sociallogin.user
        extra_data = sociallogin.account.extra_data

        user.email = user.email or extra_data.get('email')
        user.first_name = user.first_name or extra_data.get('given_name', '')
        user.last_name = user.last_name or extra_data.get('family_name', '')
        user.username = ''  # Avoid any username generation
        user.is_active = True
        user.save()
        return user


class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True  # Allow regular signup too

    def clean_username(self, username):
        return ''  # Explicitly remove username requirement
