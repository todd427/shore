from django.urls import path
from .views import questionnaire_view

urlpatterns = [
    
    path('<slug:code>/', questionnaire_view, name='take_questionnaire'),
]


from .views import results_dashboard, export_csv

urlpatterns += [
    path('<slug:code>/results/', results_dashboard, name='results_dashboard'),
    path('<slug:code>/export/', export_csv, name='export_csv'),
]
