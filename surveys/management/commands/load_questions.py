import json
from django.core.management.base import BaseCommand
from surveys.models import Questionnaire, Question

class Command(BaseCommand):
    help = 'Load questionnaire and questions from questions.json'

    def handle(self, *args, **kwargs):
        # Define the questionnaire metadata
        code = "feyman"
        title = "Feyman-Heisenberg Personality Questionnaire"
        description = "Understanding social media personality traits and behaviors."

        # Create or get the questionnaire
        questionnaire, created = Questionnaire.objects.get_or_create(
            code=code,
            defaults={'title': title, 'description': description}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created questionnaire: {title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Using existing questionnaire: {title}'))

        # Load questions from file
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)

        added = 0
        for q in questions:
            obj, is_new = Question.objects.get_or_create(
                questionnaire=questionnaire,
                text=q["text"],
                section=q["section"]
            )
            if is_new:
                added += 1

        self.stdout.write(self.style.SUCCESS(f'{added} questions loaded into questionnaire "{title}".'))
