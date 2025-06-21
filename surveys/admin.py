# surveys/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Section, Survey  # your new survey/section models
from polls.models import Question as Poll  # polls app question


from .models import Questionnaire, Question, Response

from django.urls import reverse, NoReverseMatch

from .models import Survey, Section, SurveySection, SectionPoll

class QuestionnaireAdmin(admin.ModelAdmin):

    list_display = ('title', 'code', 'view_results_link', 'export_csv_link')  # ✅ Must include this


    def view_results_link(self, obj):
        if not obj.code:
            return "—"
        try:
            url = reverse('results_dashboard', args=[obj.code])
            return format_html('<a href="{}" target="_blank">View Results</a>', url)
        except NoReverseMatch:
            return "Invalid code"
    view_results_link.short_description = "Results"

    
    def export_csv_link(self, obj):
        if not obj.code:
            return "—"
        try:
            url = reverse('export_csv', args=[obj.code])
            return format_html('<a href="{}">⬇️ Export CSV</a>', url)
        except NoReverseMatch:
            return "Invalid code"
    export_csv_link.short_description = "Export"


class SurveySectionInline(admin.TabularInline):
    model = SurveySection
    extra = 1

class SurveyAdmin(admin.ModelAdmin):
    inlines = [SurveySectionInline]

class SectionPollInline(admin.TabularInline):
    model = SectionPoll
    extra = 1

class SectionAdmin(admin.ModelAdmin):
    inlines = [SectionPollInline]

    

admin.site.register(Section, SectionAdmin)
admin.site.register(Survey, SurveyAdmin)

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question)
admin.site.register(Response)

from .models import ProgrammerResponse
admin.site.register(ProgrammerResponse)

