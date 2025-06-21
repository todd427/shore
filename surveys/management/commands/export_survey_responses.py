# surveys/management/commands/export_survey_responses.py

from django.core.management.base import BaseCommand
from surveys.models import SurveyResponse, Survey
from polls.models import Question as Poll, Choice

import csv

class Command(BaseCommand):
    help = "Export survey responses to CSV (with question and choice text)"

    def add_arguments(self, parser):
        parser.add_argument("slug", help="Slug of the survey to export")

    def handle(self, *args, **options):
        survey = Survey.objects.get(slug=options["slug"])
        filename = f"{survey.slug}_responses.csv"
        responses = SurveyResponse.objects.filter(survey=survey)
        poll_ids = set()
        for r in responses:
            poll_ids.update(r.answers.keys())
        poll_ids = sorted(poll_ids, key=int)  # so polls are in order

        # Build header with question text
        header = ["submitted_at"]
        poll_id_to_text = {}
        for pid in poll_ids:
            poll = Poll.objects.get(id=pid)
            poll_id_to_text[pid] = poll.question_text
            header.append(f"{poll.question_text} (poll_{pid})")

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for response in responses:
                row = [response.submitted_at]
                for pid in poll_ids:
                    choice_id = response.answers.get(pid)
                    if choice_id:
                        try:
                            choice = Choice.objects.get(id=choice_id)
                            row.append(choice.choice_text)
                        except Choice.DoesNotExist:
                            row.append(f"Choice {choice_id}")
                    else:
                        row.append("")
                writer.writerow(row)
        self.stdout.write(self.style.SUCCESS(f"Exported to {filename}"))
