from django.contrib import admin
from .models import Questionnaire, Question, Response

admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(Response)
