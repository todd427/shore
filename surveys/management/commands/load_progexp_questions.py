from django.core.management.base import BaseCommand
from surveys.models import Questionnaire, Question

class Command(BaseCommand):
    help = 'Load Programmer Experience Questionnaire and its questions'

    def handle(self, *args, **options):
        qnr, created = Questionnaire.objects.get_or_create(
            code='progexp',
            defaults={'title': 'Programmer Experience Questionnaire'}
        )

        if not created:
            self.stdout.write(self.style.WARNING("Questionnaire already exists. Skipping creation."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Created questionnaire: {qnr.title}"))

        questions = [
            # Section 1: General Background
            ("General Background", "First Name:", "short_text"),
            ("General Background", "Last Name:", "short_text"),
            ("General Background", "Age:", "number"),
            ("General Background", "Years of experience:", "select"),
            ("General Background", "Primary language:", "short_text"),
            ("General Background", "Other languages (check all that apply):", "checkbox_multiple"),

            # Section 2: Problem-Solving & Algorithms
            ("Problem-Solving & Algorithms", "Can you implement basic algorithms?", "select"),
            ("Problem-Solving & Algorithms", "Used complex data structures?", "select"),
            ("Problem-Solving & Algorithms", "Do you solve coding challenges?", "select"),

            # Section 3: Software Development Practices
            ("Software Development Practices", "Familiarity with Git:", "select"),
            ("Software Development Practices", "Worked with CI/CD pipelines?", "select"),
            ("Software Development Practices", "How do you test code?", "select"),

            # Section 4: Project & Collaboration Experience
            ("Project & Collaboration Experience", "Open-source contributions?", "select"),
            ("Project & Collaboration Experience", "Largest project you've worked on:", "long_text"),
            ("Project & Collaboration Experience", "Experience with Agile/Scrum?", "select"),

            # Section 5: System Design & Deployment
            ("System Design & Deployment", "Designed a system architecture?", "select"),
            ("System Design & Deployment", "Familiarity with concepts:", "select"),
            ("System Design & Deployment", "Deployment experience?", "select"),
            ("System Design & Deployment", "Platforms/tools used:", "checkbox_multiple"),

            # Section 6: Learning & Interests
            ("Learning & Interests", "Favorite development areas:", "checkbox_multiple"),
            ("Learning & Interests", "How often do you learn new tech?", "select"),
        ]

        for section, text, qtype in questions:
            Question.objects.get_or_create(
                questionnaire=qnr,
                text=text.strip(),
                section=section.strip(),
                defaults={'input_type': qtype}
            )

        self.stdout.write(self.style.SUCCESS("All questions loaded."))
