import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # Replace with your project
django.setup()

from surveys.models import Questionnaire, Question

def load_questions(json_path, questionnaire_code, title, description):
    with open(json_path) as f:
        data = json.load(f)

    qn, created = Questionnaire.objects.get_or_create(
        code=questionnaire_code,
        defaults={'title': title, 'description': description}
    )

    for item in data:
        Question.objects.get_or_create(
            questionnaire=qn,
            text=item['text'],
            section=item['section']
        )

    print(f"Loaded {len(data)} questions into questionnaire '{qn.title}'")

# Example usage
if __name__ == "__main__":
    load_questions("questions.json", "feynman-drummelberg",
                   "Feynman-Drummelberg Personality Questionnaire",
                   "A psychometric tool for evaluating social media behavior.")
