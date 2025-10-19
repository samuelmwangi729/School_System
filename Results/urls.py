from django.urls import path
from Results.views import ResultsApiView,InstitutionResultView

urlpatterns = [
    path('results',ResultsApiView.as_view(),name='results'),
    path('results/institution',InstitutionResultView.as_view(),name='institution_results'),
]
