from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

CustomUser = get_user_model()


class CustomUserTests(TestCase):
    
    def setUp(self):
        print(f"\nRunning tests in: {self.__class__.__name__}")

    def test_create_user(self):
        print(self._testMethodName)
        user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_create_superuser(self):
        print(self._testMethodName)
        admin_user = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass"
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)


class SignupTests(TestCase):
   
    def setUp(self):
        print(f"\nRunning tests in: {self.__class__.__name__}")

    def test_signup_view_status_code(self):
        print(self._testMethodName)
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_template_used(self):
        print(self._testMethodName)
        response = self.client.get(reverse("account_signup"))
        self.assertTemplateUsed(response, "account/signup.html")

    def test_signup_creates_user(self):
        print(self._testMethodName)
        response = self.client.post(reverse("account_signup"), {
            "email": "newuser@example.com",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())


class LoginLogoutTests(TestCase):
    
    def setUp(self):
        print(f"\nRunning tests in: {self.__class__.__name__}")
        self.user = CustomUser.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="loginpass123"
        )
        # Allauth requires email verification for login to succeed
        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            verified=True,
            primary=True,
        )

    def test_login_view_status_code(self):
        print(self._testMethodName)
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        print(self._testMethodName)
        login = self.client.login(email="login@example.com", password="loginpass123")
        self.assertTrue(login)

    def test_logout(self):
        print(self._testMethodName)
        self.client.login(username="loginuser", password="loginpass123")
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 200)


class URLTests(TestCase):

    def setUp(self):
        print(f"\nRunning tests in: {self.__class__.__name__}")

    def test_login_url(self):
        print(self._testMethodName)
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_url_redirect(self):
        print(self._testMethodName)
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 302)  # Allauth logout redirects

    def test_logout_url(self):
        print(self._testMethodName)
        response = self.client.get(reverse("account_logout"), follow=True)
        self.assertEqual(response.status_code, 200)


    def test_signup_url(self):
        print(self._testMethodName)
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)
