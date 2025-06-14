from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.html import escape

import hashlib
import json
import csv
import html

from .models import Questionnaire, Question, Response, AGE_CHOICES
from .forms import DynamicSurveyForm

# Utility to generate UUID
def generate_uuid(request):
    ip = request.META.get('REMOTE_ADDR', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    base = ip + user_agent
    return "uuid-" + hashlib.sha256(base.encode()).hexdigest()[:16]

# Main questionnaire view with DynamicSurveyForm
def questionnaire_view(request, code):
    print("Running test: questionnaire_view")
    questionnaire = get_object_or_404(Questionnaire, code=code)

    if request.method == 'POST':
        form = DynamicSurveyForm(questionnaire, request.POST)
        if form.is_valid():
            scores = {}
            counts = {}
            total_score = 0

            for q in Question.objects.filter(questionnaire=questionnaire):
                val = int(form.cleaned_data[f"q_{q.id}"])
                scores[q.section] = scores.get(q.section, 0) + val
                counts[q.section] = counts.get(q.section, 0) + 1
                total_score += val

            for section in scores:
                scores[section] = round(scores[section] / counts[section], 2)

            base_uuid = generate_uuid(request)
            suffix = 0
            new_uuid = base_uuid
            while Response.objects.filter(uuid=new_uuid).exists():
                suffix += 1
                new_uuid = f"{base_uuid}-{suffix}"

            Response.objects.create(
                uuid=new_uuid,
                age=form.cleaned_data["age"],
                questionnaire=questionnaire,
                total_score=total_score,
                scores=scores,
                submitted_at=timezone.now()
            )

            return render(request, "surveys/thank_you.html", {"score": total_score, "uuid": new_uuid, "scores": scores})
    else:
        form = DynamicSurveyForm(questionnaire)

    return render(request, "surveys/questionnaire.html", {
        "form": form,
        "questionnaire": questionnaire
    })

# JSON API of all responses
@staff_member_required
def response_list(request):
    print("Running test: response_list")
    responses = Response.objects.all().order_by('-submitted_at')
    data = [
        {
            "uuid": r.uuid,
            "age": r.age,
            "score": r.total_score,
            "sections": r.scores,
            "time": r.submitted_at.isoformat()
        }
        for r in responses
    ]
    return JsonResponse(data, safe=False)

# Web dashboard of results for a specific questionnaire
@staff_member_required
def results_dashboard(request, code):
    print("Running test: results_dashboard")
    questionnaire = get_object_or_404(Questionnaire, code=code)
    responses = Response.objects.filter(questionnaire=questionnaire).order_by('-submitted_at')
    return render(request, "surveys/results_dashboard.html", {
        "questionnaire": questionnaire,
        "responses": responses
    })

# CSV export of results for a specific questionnaire
@staff_member_required
def export_csv(request, code):
    print("Running test: export_csv")
    questionnaire = get_object_or_404(Questionnaire, code=code)
    responses = Response.objects.filter(questionnaire=questionnaire).order_by('-submitted_at')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{code}_results.csv"'

    writer = csv.writer(response)
    writer.writerow(["UUID", "Age", "Submitted At", "Total Score", "Section Scores"])
    for r in responses:
        writer.writerow([
            r.uuid,
            r.age,
            r.submitted_at.strftime("%Y-%m-%d %H:%M:%S"),
            r.total_score,
            json.dumps(r.scores)
        ])
    return response

# ================= TESTS ===================



class SurveyTests(TestCase):
    def setUp(self):
        print("Setting up test database...")
        self.qnr = Questionnaire.objects.create(
            code="persquiz",
            title="Personality & Social Media Survey",
            description=""
        )

    def test_questionnaire_view_renders(self):
        print("Running: test_questionnaire_view_renders")
        response = self.client.get(reverse('questionnaire', kwargs={'code': 'persquiz'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, escape(self.qnr.title))

    def test_questionnaire_404_for_unknown_code(self):
        print("Running: test_questionnaire_404_for_unknown_code")
        response = self.client.get(reverse('questionnaire', kwargs={'code': 'notfound'}))
        self.assertEqual(response.status_code, 404)

    def test_form_post_creates_response(self):
        print("Running: test_form_post_creates_response")
        Question.objects.create(questionnaire=self.qnr, text="Q1", section="A")
        Question.objects.create(questionnaire=self.qnr, text="Q2", section="A")

        form_data = {
            'age': '25–34',
            'q_1': '3',
            'q_2': '4'
        }
        response = self.client.post(reverse('questionnaire', kwargs={'code': 'persquiz'}), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank You!")

    def test_response_list_json(self):
        print("Running: test_response_list_json")
        self.client.force_login(self._create_admin_user())
        response = self.client.get(reverse('response_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_results_dashboard_view(self):
        print("Running: test_results_dashboard_view")
        self.client.force_login(self._create_admin_user())
        response = self.client.get(reverse('results_dashboard', kwargs={'code': 'persquiz'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, escape(self.qnr.title))

    def test_export_csv_view(self):
        print("Running: test_export_csv_view")
        self.client.force_login(self._create_admin_user())
        response = self.client.get(reverse('export_csv', kwargs={'code': 'persquiz'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response['Content-Type'])
        self.assertIn('Content-Disposition', response.headers)

    def _create_admin_user(self):
        User = get_user_model()
        return User.objects.create_superuser('admin', 'admin@example.com', 'password')

    def test_progexp_questionnaire_view_renders(self):
        response = self.client.get('/surveys/progexp/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Programmer Experience Questionnaire")

