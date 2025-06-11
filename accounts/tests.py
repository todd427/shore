from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()

class CustomUserModelTests(TestCase):
    print("CustomUserModelTests")
    def test_create_user(self):
        print("test_create_user")
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("securepass123"))

    def test_create_superuser(self):
        print("test_create_superuser")
        superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass"
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

class CustomUserCreationFormTests(TestCase):
    print("CustomUserCreationFormTests")
    def test_valid_form(self):
        print("test_valid_form")
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        print("test_password_mismatch")
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "pass1",
            "password2": "pass2",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

class CustomUserChangeFormTests(TestCase):
    print("CustomUserChangeFormTests")
    def test_change_email(self):
        print("test_change_email")
        user = User.objects.create_user(
            username="testuser",
            email="old@example.com",
            password="somepass"
        )
        form_data = {
            "username": "testuser",
            "email": "new@example.com",
        }
        form = CustomUserChangeForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.email, "new@example.com")
