from django.urls import path
from .views import questionnaire_view, response_list, results_dashboard, export_csv 

urlpatterns = [
    path('results/', response_list, name='response_list'),
    path('<slug:code>/', questionnaire_view, name='questionnaire'),
]


from .views import results_dashboard, export_csv

urlpatterns += [
    path('<slug:code>/results/', results_dashboard, name='results_dashboard'),
    path('<slug:code>/export/', export_csv, name='export_csv'),
]
