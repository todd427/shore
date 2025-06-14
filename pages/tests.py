from django.test import TestCase
from django.urls import reverse, resolve
from .views import HomePageView, AboutPageView

# HomePageViewTests
# commit test trigger
class HomePageViewTests(TestCase):
    print("\n=== HomePageViewTests ===")
    def test_home_page_status_code(self):
        print("Running: test_home_page_status_code")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template_used(self):
        print("Running: test_home_page_template_used")
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_base_template_extends(self):
        print("Running: test_home_page_base_template_extends")
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base.html")  # inherited template

    def test_home_page_content(self):
        print("Running: test_home_page_content")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Welcome to")  # adjust based on your actual content

    def test_home_page_url_resolves_to_home_page_view(self):
        print("Running: test_home_page_url_resolves_to_home_page_view")
        view = resolve("/")
        self.assertEqual(view.func.view_class, HomePageView)


class AboutPageTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n=== Running AboutPageTests ===")

    def setUp(self):
        self.url = reverse('about')

    def test_about_page_status_code(self):
        print("Running: test_about_page_status_code")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_about_page_template_used(self):
        print("Running: test_about_page_template_used")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'about.html')

    def test_about_page_contains_bootstrap_classes(self):
        print("Running: test_about_page_contains_bootstrap_classes")
        response = self.client.get(self.url)
        content = response.content.decode()
        self.assertIn('container', content)
        self.assertIn('row', content)
        self.assertIn('img-fluid', content)
        self.assertIn('rounded-circle', content)
        self.assertIn('lead', content)

    def test_about_page_displays_author_name(self):
        print("Running: test_about_page_displays_author_name")
        response = self.client.get(self.url)
        self.assertContains(response, "Todd McCaffrey")
