from django.test import TestCase
from .models import Questionnaire

class QuestionnaireModelTest(TestCase):
    def setUp(self):
        Questionnaire.objects.create(title="Sample Questionnaire")

    def test_questionnaire_creation(self):
        """Test if a Questionnaire instance can be created and retrieved"""
        q = Questionnaire.objects.get(title="Sample Questionnaire")
        self.assertEqual(q.title, "Sample Questionnaire")
        print(f"[Test] Retrieved Questionnaire title: {q.title}")

    def test_questionnaire_count(self):
        """Test if exactly one Questionnaire is in the database"""
        count = Questionnaire.objects.count()
        self.assertEqual(count, 1)
        print(f"[Test] Number of Questionnaire records: {count}")
