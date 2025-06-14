from django.urls import path
from .views import questionnaire_view, response_list, results_dashboard, export_csv

urlpatterns = [
    path('results/json/', response_list, name='response_list'),
    path('results/', results_dashboard, name='results_dashboard'),
    path('results/export/', export_csv, name='export_csv'),
    path('<slug:code>/', questionnaire_view, name='questionnaire'),
]
