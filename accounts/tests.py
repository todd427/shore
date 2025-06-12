from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm

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

class SignUpTests(TestCase):

    def setUp(self):
        print(f"\nRunning tests in: {self.__class__.__name__}")

    def test_signup_view_status_code(self):
        print(self._testMethodName)
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_template(self):
        print(self._testMethodName)
        response = self.client.get(reverse("signup"))
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form(self):
        print(self._testMethodName)
        form = CustomUserCreationForm(data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "complexpass123",
            "password2": "complexpass123"
        })
        self.assertTrue(form.is_valid())

    def test_signup_creates_user(self):
        print(self._testMethodName)
        self.client.post(reverse("signup"), {
            "username": "newuser2",
            "email": "newuser2@example.com",
            "password1": "complexpass123",
            "password2": "complexpass123"
        })
        self.assertTrue(CustomUser.objects.filter(username="newuser2").exists())

class LoginLogoutTests(TestCase):

    def setUp(self):
        print(f"\nRunning tests in: {self.__class__.__name__}")
        self.user = CustomUser.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="loginpass123"
        )

    def test_login(self):
        print(self._testMethodName)
        login = self.client.login(username="loginuser", password="loginpass123")
        self.assertTrue(login)

    def test_logout(self):
        print(self._testMethodName)
        self.client.login(username="loginuser", password="loginpass123")
        self.client.logout()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

class URLTests(TestCase):

    def setUp(self):
        print(f"\nRunning tests in: {self.__class__.__name__}")

    def test_login_url_resolves(self):
        print(self._testMethodName)
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_url_resolves(self):
        print(self._testMethodName)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
