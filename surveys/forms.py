from django import forms
from .models import Question, AGE_CHOICES

class DynamicSurveyForm(forms.Form):
    age = forms.ChoiceField(choices=[("", "-- Select --")] + AGE_CHOICES, label="Age Group")

    def __init__(self, questionnaire, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.questionnaire = questionnaire
        questions = Question.objects.filter(questionnaire=questionnaire)
        for q in questions:
            field_name = f"q_{q.id}"
            self.fields[field_name] = forms.ChoiceField(
                label=q.text,
                choices=[("", "--")] + [(i, str(i)) for i in range(1, 6)],
                widget=forms.RadioSelect,
                required=True
            )
