from django.db import models

AGE_CHOICES = [
    ("0–2", "0–2 (Infant)"),
    ("3–12", "3–12 (Child)"),
    ("13–17", "13–17 (Teen)"),
    ("18–24", "18–24 (Young Adult)"),
    ("25–34", "25–34 (Early Adult)"),
    ("35–44", "35–44 (Middle Adult)"),
    ("45–54", "45–54 (Older Adult)"),
    ("55–64", "55–64 (Senior)"),
    ("65+", "65+ (Elder)"),
]

class Questionnaire(models.Model):
    code = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    text = models.TextField()
    section = models.CharField(max_length=200, blank=True)
    input_type = models.CharField(
        max_length=30,
        choices=[
            ('short_text', 'Short Text'),
            ('long_text', 'Long Text'),
            ('select', 'Select'),
            ('checkbox_multiple', 'Checkboxes'),
            ('number', 'Number'),
        ],
        default='short_text'
    )

    def __str__(self):
        return f"{self.section}: {self.text[:40]}"

class Response(models.Model):
    uuid = models.CharField(max_length=64)
    age = models.CharField(max_length=16, choices=AGE_CHOICES)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    total_score = models.FloatField()
    scores = models.JSONField()

class ProgrammerResponse(models.Model):
    submitted_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    years = models.CharField(max_length=10)
    primary_language = models.CharField(max_length=100, blank=True)
    languages = models.JSONField(default=list, blank=True)
    other_language = models.CharField(max_length=100, blank=True)
    algorithms = models.CharField(max_length=50)
    data_structures = models.CharField(max_length=50)
    challenges = models.CharField(max_length=50)
    git = models.CharField(max_length=50)
    ci_cd = models.CharField(max_length=50)
    testing = models.CharField(max_length=50)
    open_source = models.CharField(max_length=50)
    largest_project = models.TextField(blank=True)
    agile = models.CharField(max_length=50)
    architecture = models.CharField(max_length=50)
    concepts = models.CharField(max_length=50)
    deployment = models.CharField(max_length=50)
    platforms = models.JSONField(default=list, blank=True)
    platform_other = models.CharField(max_length=100, blank=True)
    interests = models.JSONField(default=list, blank=True)
    interests_other = models.CharField(max_length=100, blank=True)
    learning = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.age})"