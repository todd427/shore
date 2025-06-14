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
    section = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.section}: {self.text[:40]}"

class Response(models.Model):
    uuid = models.CharField(max_length=64)
    age = models.CharField(max_length=16, choices=AGE_CHOICES)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    total_score = models.FloatField()
    scores = models.JSONField()
