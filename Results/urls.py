from django.urls import path
from Results.views import ResultsApiView

urlpatterns = [
    path('results',ResultsApiView.as_view(),name='results')
]
