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

from django import forms

class ProgrammerSurveyForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    age = forms.IntegerField(label="Age", min_value=18, max_value=100)
    
    YEARS = [
        ("<1", "Less than 1 year"),
        ("1–2", "1–2 years"),
        ("3–5", "3–5 years"),
        ("6–10", "6–10 years"),
        ("10+", "10+ years"),
    ]
    years = forms.ChoiceField(label="Years of experience", choices=YEARS)

    primary_language = forms.CharField(label="Primary language", required=False)

    LANGUAGES = [
        ("Python", "Python"),
        ("JavaScript", "JavaScript"),
        ("Java", "Java"),
        ("C++", "C/C++"),
        ("Go", "Go"),
        ("Rust", "Rust"),
    ]
    languages = forms.MultipleChoiceField(
        label="Other languages", 
        choices=LANGUAGES, 
        widget=forms.CheckboxSelectMultiple, 
        required=False)
    other_language = forms.CharField(label="Other language", required=False)

    ALGORITHMS = list(reversed([
        ("Yes", "Yes"),
        ("With some help", "With some help"),
        ("Not confidently", "Not confidently"),
    ]))
    algorithms = forms.ChoiceField(
        label="Can you implement basic algorithms?", 
        choices=ALGORITHMS, 
        widget=forms.RadioSelect,
        required=True)

    DATA_STRUCTURES = list(reversed([
        ("Frequently", "Frequently"),
        ("Occasionally", "Occasionally"),
        ("Only in tutorials", "Only in tutorials"),
        ("Never", "Never"),
    ]))
    data_structures = forms.ChoiceField(
        label="Used complex data structures?", 
        choices=DATA_STRUCTURES, 
        widget=forms.RadioSelect,
        required=True)

    CHALLENGES = list(reversed([
        ("Yes, weekly", "Yes, weekly"),
        ("Occasionally", "Occasionally"),
        ("Rarely", "Rarely"),
        ("Never", "Never"),
    ]))
    challenges = forms.ChoiceField(
        label="Do you solve coding challenges?", 
        choices=CHALLENGES, 
        widget=forms.RadioSelect,
        required=True)

    GIT = list(reversed([
        ("Expert", "Expert"),
        ("Basic commands", "Basic commands"),
        ("Learning", "Learning"),
        ("Never used", "Never used"),
    ]))
    git = forms.ChoiceField(
        label="Familiarity with Git", 
        choices=GIT, 
        widget=forms.RadioSelect,
        required=True)

    CICD = list(reversed([
        ("Set it up myself", "Set it up myself"),
        ("Used in a team", "Used in a team"),
        ("Not yet", "Not yet"),
    ]))
    ci_cd = forms.ChoiceField(
        label="Worked with CI/CD pipelines?", 
        choices=CICD, 
        widget=forms.RadioSelect,
        required=True)

    TESTING = list(reversed([
        ("Unit tests", "Unit tests"),
        ("Integration tests", "Integration tests"),
        ("Manual testing only", "Manual testing only"),
        ("Rarely test", "Rarely test"),
    ]))
    testing = forms.ChoiceField(
        label="How do you test code?", 
        choices=TESTING, 
        widget=forms.RadioSelect,
        required=True)

    OPEN_SOURCE = list(reversed([
        ("Yes", "Yes"),
        ("Interested", "Interested"),
        ("No", "No"),
    ]))
    open_source = forms.ChoiceField(
        label="Open-source contributions?", 
        choices=OPEN_SOURCE, 
        widget=forms.RadioSelect,
        required=True)
    largest_project = forms.CharField(label="Largest project", widget=forms.Textarea, required=False)

    AGILE = list(reversed([
        ("Yes", "Yes"),
        ("Somewhat familiar", "Somewhat familiar"),
        ("No", "No"),
    ]))
    agile = forms.ChoiceField(
        label="Experience with Agile/Scrum?", 
        choices=AGILE, 
        widget=forms.RadioSelect,
        required=True)

    ARCHITECTURE = list(reversed([
        ("Yes, professionally", "Yes, professionally"),
        ("Yes, personal projects", "Yes, personal projects"),
        ("Not yet", "Not yet"),
    ]))
    architecture = forms.ChoiceField(
        label="Designed a system architecture?", 
        choices=ARCHITECTURE, 
        widget=forms.RadioSelect,
        required=True)

    CONCEPTS = list(reversed([
        ("Strong understanding", "Strong understanding"),
        ("Basic familiarity", "Basic familiarity"),
        ("No", "No"),
    ]))
    concepts = forms.ChoiceField(
        label="Familiarity with system design concepts?", 
        choices=CONCEPTS, 
        widget=forms.RadioSelect,
        required=True)

    DEPLOYMENT = list(reversed([
        ("Frequently", "Frequently"),
        ("A few times", "A few times"),
        ("Never", "Never"),
    ]))
    deployment = forms.ChoiceField(
        label="Deployment experience?", 
        choices=DEPLOYMENT, 
        widget=forms.RadioSelect,
        required=True)

    PLATFORMS = list(reversed([
        ("AWS", "AWS"),
        ("Docker", "Docker"),
        ("Kubernetes", "Kubernetes"),
        ("GitHub Actions", "GitHub Actions"),
    ]))
    platforms = forms.MultipleChoiceField(label="Platforms/tools used", choices=PLATFORMS, widget=forms.CheckboxSelectMultiple, required=False)
    platform_other = forms.CharField(label="Other platform", required=False)

    INTERESTS = list(reversed([
        ("Web", "Web Development"),
        ("Game", "Game Development"),
        ("AI", "Machine Learning / AI"),
        ("DevOps", "DevOps"),
    ]))
    interests = forms.MultipleChoiceField(
        label="Favorite dev areas", 
        choices=INTERESTS, 
        widget=forms.CheckboxSelectMultiple, 
        required=False)
    interests_other = forms.CharField(label="Other interests", required=False)

    LEARNING = list(reversed([
        ("Constantly", "Constantly"),
        ("Every few months", "Every few months"),
        ("When needed", "When needed"),
        ("Rarely", "Rarely"),
    ]))
    learning = forms.ChoiceField(label="How often do you learn new tech?", choices=LEARNING, widget=forms.RadioSelect)
