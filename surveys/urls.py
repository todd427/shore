from django.urls import path

from .views import questionnaire_view, results_dashboard, export_csv, response_list

urlpatterns = [
    path('results/json/', response_list, name='response_list'),
    path('<slug:code>/results/', results_dashboard, name='results_dashboard'),
    path('<slug:code>/export/', export_csv, name='export_csv'),
    path('<slug:code>/', questionnaire_view, name='questionnaire'),
    path('<slug:code>/results/', results_dashboard, name='results_dashboard'),
    path('<slug:code>/export/', export_csv, name='export_csv'),

]
