from django.shortcuts import render, get_object_or_404
from .models import Questionnaire, Question, Response
from .forms import DynamicSurveyForm
import hashlib

def generate_uuid(request):
    ip = request.META.get('REMOTE_ADDR', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    base = ip + user_agent
    return "uuid-" + hashlib.sha256(base.encode()).hexdigest()[:16]

def questionnaire_view(request, code):
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

            Response.objects.create(
                uuid=generate_uuid(request),
                age=form.cleaned_data["age"],
                questionnaire=questionnaire,
                total_score=total_score,
                scores=scores
            )
            return render(request, "surveys/thank_you.html", {"score": total_score})
    else:
        form = DynamicSurveyForm(questionnaire)

    return render(request, "surveys/questionnaire.html", {
        "form": form,
        "questionnaire": questionnaire
    })


import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Questionnaire, Response

def results_dashboard(request, code):
    questionnaire = get_object_or_404(Questionnaire, code=code)
    responses = Response.objects.filter(questionnaire=questionnaire)
    return render(request, "surveys/results_dashboard.html", {
        "questionnaire": questionnaire,
        "responses": responses
    })

def export_csv(request, code):
    questionnaire = get_object_or_404(Questionnaire, code=code)
    responses = Response.objects.filter(questionnaire=questionnaire)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{code}_results.csv"'

    writer = csv.writer(response)
    writer.writerow(["UUID", "Age", "Submitted At", "Total Score", "Section Scores"])
    for r in responses:
        writer.writerow([
            r.uuid, r.age, r.submitted_at.strftime("%Y-%m-%d %H:%M:%S"), r.total_score, r.scores
        ])
    return response

from django.shortcuts import render, get_object_or_404, redirect
from .models import Questionnaire, Question, Response, AGE_CHOICES
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

@csrf_exempt  # only if testing without CSRF token; remove in production
def questionnaire(request, code):
    questionnaire = get_object_or_404(Questionnaire, code=code)
    questions = Question.objects.filter(questionnaire=questionnaire)

    if request.method == "POST":
        age = request.POST.get("age")
        raw_uuid = request.POST.get("uuid")
        scores = {}
        total_score = 0

        # Group questions by section
        for index, q in enumerate(questions, start=1):
            key = f"q{index}"
            val = request.POST.get(key)
            if not val or not val.isdigit():
                continue
            val = int(val)
            section = q.section
            scores.setdefault(section, 0)
            scores[section] += val
            total_score += val

        # Deduplicate UUIDs
        base_uuid = raw_uuid
        suffix = 0
        new_uuid = base_uuid
        while Response.objects.filter(uuid=new_uuid).exists():
            suffix += 1
            new_uuid = f"{base_uuid}-{suffix}"

        # Save response
        Response.objects.create(
            uuid=new_uuid,
            age=age,
            questionnaire=questionnaire,
            total_score=total_score,
            scores=scores,
            submitted_at=timezone.now()
        )

        return render(request, "surveys/thank_you.html", {
            "uuid": new_uuid,
            "total": total_score,
            "scores": scores,
        })

    return render(request, "surveys/take_questionnaire.html", {
        "questionnaire": questionnaire,
        "questions": questions,
        "age_choices": AGE_CHOICES,
    })
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import Response

@staff_member_required  # requires staff login to access
def response_list(request):
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

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
import csv
from django.http import HttpResponse

# Already imported: Response

@staff_member_required
def results_dashboard(request):
    responses = Response.objects.all().order_by('-submitted_at')
    return render(request, 'surveys/results_dashboard.html', {
        'responses': responses
    })

@staff_member_required
def export_csv(request):
    responses = Response.objects.all().order_by('-submitted_at')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="questionnaire_results.csv"'

    writer = csv.writer(response)
    writer.writerow(['UUID', 'Age', 'Total Score', 'Scores by Section', 'Submitted At'])

    for r in responses:
        writer.writerow([
            r.uuid,
            r.age,
            r.total_score,
            json.dumps(r.scores),
            r.submitted_at.isoformat()
        ])

    return response
