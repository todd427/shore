from django.urls import path

from .views import (
    questionnaire_view, 
    results_dashboard, 
    export_csv, 
    response_list, 
    programmer_questionnaire_view, 
    take_survey, 
    show_survey
)

urlpatterns = [
    path('results/json/', response_list, name='response_list'),
    path('progexp/', programmer_questionnaire_view, name='programmer_experience'),
    path('<slug:code>/results/', results_dashboard, name='results_dashboard'),
    path('<slug:code>/export/', export_csv, name='export_csv'),
    path('<slug:code>/', questionnaire_view, name='questionnaire'),
    path('<slug:code>/results/', results_dashboard, name='results_dashboard'),
    path('<slug:code>/take/', take_survey, name='take_survey'),
    path('surveys/<slug:slug>/', show_survey, name='show_survey'),

]
