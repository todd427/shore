# surveys/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

import hashlib
import json
import csv

from .models import (
    Questionnaire, 
    Question, 
    Response, 
    AGE_CHOICES, 
    ProgrammerResponse, 
    Survey, 
    Section, 
    SectionPoll,
    SurveyResponse
)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, SurveyResponse
from polls.models import Question as Poll



from .forms import DynamicSurveyForm

# Utility to generate UUID

def generate_uuid(request):
    ip = request.META.get('REMOTE_ADDR', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    base = ip + user_agent
    return "uuid-" + hashlib.sha256(base.encode()).hexdigest()[:16]

# Main questionnaire view with DynamicSurveyForm

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

            # Handle UUID collision
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
    questionnaire = get_object_or_404(Questionnaire, code=code)
    responses = Response.objects.filter(questionnaire=questionnaire).order_by('-submitted_at')
    return render(request, "surveys/results_dashboard.html", {
        "questionnaire": questionnaire,
        "responses": responses,
        "num_responses": responses.count()
    })


# CSV export of results for a specific questionnaire

@staff_member_required
def export_csv(request, code):
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

from .forms import ProgrammerSurveyForm

def programmer_questionnaire_view(request):
    submitted = False
    if request.method == 'POST':
        form = ProgrammerSurveyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ProgrammerResponse.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                age=data['age'],
                years=data['years'],
                primary_language=data['primary_language'],
                languages=data['languages'],
                other_language=data['other_language'],
                algorithms=data['algorithms'],
                data_structures=data['data_structures'],
                challenges=data['challenges'],
                git=data['git'],
                ci_cd=data['ci_cd'],
                testing=data['testing'],
                open_source=data['open_source'],
                largest_project=data['largest_project'],
                agile=data['agile'],
                architecture=data['architecture'],
                concepts=data['concepts'],
                deployment=data['deployment'],
                platforms=data['platforms'],
                platform_other=data['platform_other'],
                interests=data['interests'],
                interests_other=data['interests_other'],
                learning=data['learning'],
            )
            submitted = True
    else:
        form = ProgrammerSurveyForm()
    return render(request, 'surveys/questionnaire_progexp.html', {
        'form': form,
        'submitted': submitted
    })

def show_survey(request, slug):
    survey = get_object_or_404(Survey, slug=slug)
    sections = survey.sections.all().order_by('surveysection__order')

    if request.method == 'POST':
        # Build a dictionary of answers: {poll_id: choice_id}
        answers = {}
        for section in sections:
            polls = section.polls.all().order_by('sectionpoll__order')
            for poll in polls:
                val = request.POST.get(f'poll_{poll.id}')
                if val:
                    answers[str(poll.id)] = val
        # Save response only if answers for all polls
        if len(answers) == sum(section.polls.count() for section in sections):
            SurveyResponse.objects.create(survey=survey, answers=answers)
            return render(request, 'surveys/thank_you.html', {'survey': survey})
        else:
            # Show form again with error
            error = "Please answer all questions."
            return render(request, 'surveys/show_survey.html', {
                'survey': survey,
                'sections': sections,
                'error': error,
            })
            
    return render(request, 'surveys/show_survey.html', {
        'survey': survey,
        'sections': sections
    })

def take_survey(request, survey_slug):
    survey = get_object_or_404(Survey, slug=survey_slug)
    # Prefetch related sections and polls, sorted by order
    sections = survey.sections.through.objects.filter(survey=survey).order_by('order')
    section_objs = [sp.section for sp in sections]

    # For each section, get its polls
    context_sections = []
    for section in section_objs:
        polls = section.polls.through.objects.filter(section=section).order_by('order')
        poll_objs = [p.poll for p in polls]
        context_sections.append({'section': section, 'polls': poll_objs})

    context = {
        'survey': survey,
        'sections': context_sections,
    }
    return render(request, "surveys/take_survey.html", context)
