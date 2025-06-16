from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice
from datetime import timedelta

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        future_question = Question(pub_date=timezone.now() + timedelta(days=30))
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        old_question = Question(pub_date=timezone.now() - timedelta(days=2))
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        recent_question = Question(pub_date=timezone.now() - timedelta(hours=12))
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertEqual(list(response.context['latest_question_list']), [])


    def test_past_question_displayed(self):
        Question.objects.create(question_text="Past question.", pub_date=timezone.now() - timedelta(days=1))
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "Past question.")

    def test_future_question_not_displayed(self):
        Question.objects.create(question_text="Future question.", pub_date=timezone.now() + timedelta(days=1))
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, "Future question.")


class QuestionDetailViewTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        future_question = Question.objects.create(
            question_text='Future question.',
            pub_date=timezone.now() + timedelta(days=5)
        )
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        past_question = Question.objects.create(
            question_text='Past Question.',
            pub_date=timezone.now() - timedelta(days=1)
        )
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class VoteTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text="What's up?",
            pub_date=timezone.now()
        )
        self.choice1 = Choice.objects.create(question=self.question, choice_text="Not much", votes=0)
        self.choice2 = Choice.objects.create(question=self.question, choice_text="The sky", votes=0)

    def test_vote_increments_choice(self):
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {
            'choice': self.choice1.id
        })
        self.assertRedirects(response, reverse('polls:results', args=(self.question.id,)))
        self.choice1.refresh_from_db()
        self.assertEqual(self.choice1.votes, 1)

    def test_vote_invalid_choice(self):
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {
            'choice': 999
        })
        self.assertContains(response, "You didn&#x27;t select a choice.")
