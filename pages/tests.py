from django.test import TestCase
from django.urls import reverse, resolve
from .views import HomePageView


class HomePageViewTests(TestCase):
    print("HomePageViewTests")
    def test_home_page_status_code(self):
        print("test_home_page_status_code")
        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template_used(self):
        print("test_home_page_template_used")
        response = self.client.get(reverse("pages:home"))
        self.assertTemplateUsed(response, "pages/home.html")

    def test_home_page_base_template_extends(self):
        print("test_home_page_base_template_extends")
        response = self.client.get(reverse("pages:home"))
        self.assertTemplateUsed(response, "pages/base.html")  # inherited template

    def test_home_page_content(self):
        print("test_home_page_content")
        response = self.client.get(reverse("pages:home"))
        self.assertContains(response, "Welcome to")  # adjust based on your actual content

    def test_home_page_url_resolves_to_home_page_view(self):
        print("test_home_page_url_resolves_to_home_page_view")
        view = resolve("/")
        self.assertEqual(view.func.view_class, HomePageView)