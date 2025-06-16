from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

User = get_user_model()

class SocialAppSetupMixin:
    def setUp(self):
        super().setUp()
        site, _ = Site.objects.get_or_create(id=1, defaults={
            'domain': 'localhost',
            'name': 'localhost',
        })
        if not SocialApp.objects.filter(provider="google").exists():
            app = SocialApp.objects.create(
                provider="google",
                name="Google",
                client_id="test-id",
                secret="test-secret",
            )
            app.sites.add(site)

class SignupTests(SocialAppSetupMixin, TestCase):
    def test_signup_view_status_code(self):
        print("Running test_signup_view_status_code")
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_template_used(self):
        print("Running test_signup_template_used")
        response = self.client.get(reverse("account_signup"))
        self.assertTemplateUsed(response, "account/signup.html")

class LoginLogoutTests(SocialAppSetupMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

    def test_login_view_status_code(self):
        print("Running test_login_view_status_code")
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        print("Running test_login_success")
        login_success = self.client.login(username="testuser", password="password123")
        self.assertTrue(login_success)

    def test_logout(self):
        print("Running test_logout")
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("account_logout"), follow=True)
        self.assertEqual(response.status_code, 200)

class URLTests(SocialAppSetupMixin, TestCase):
    def test_login_url(self):
        print("Running test_login_url")
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        print("Running test_logout_url")
        response = self.client.get(reverse("account_logout"))
        self.assertIn(response.status_code, [200, 302])

    def test_signup_url(self):
        print("Running test_signup_url")
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)
