from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class NoSocialSignupConfirmAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        return True
