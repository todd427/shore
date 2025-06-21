# surveys/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Section, Survey  # your new survey/section models
from .models import SurveyResponse
from polls.models import Question as Poll, Choice  # polls app question

from .models import ProgrammerResponse

from .models import Questionnaire, Question, Response

from django.urls import reverse, NoReverseMatch

from .models import Survey, Section, SurveySection, SectionPoll

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase

from .models import Survey, SurveySection, Section, SectionPoll, SurveyResponse


class SurveySectionInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SurveySection
    extra = 1
    fields = ['section', 'order']
    autocomplete_fields = ['section']

class SurveyAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [SurveySectionInline]
    list_display = ("title", "slug")
    search_fields = ("title", "slug")


class SectionPollInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SectionPoll
    extra = 1
    fields = ['poll', 'order']  # 'order' must be visible for drag&drop!
    readonly_fields = ['order'] # Optionally prevent manual edits to order
    autocomplete_fields = ['poll']


class SectionAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [SectionPollInline]
    list_display = ("name", "label")
    search_fields = ("name", "label")


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text",)
    search_fields = ("question_text",)

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

class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ("survey", "submitted_at")
    list_filter = ("survey",)
    search_fields = ("survey__title",)

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SurveyResponse, SurveyResponseAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(ProgrammerResponse)