from django.urls import path 
from Institutions.views import InstitutionView
urlpatterns = [
    path("institutions",InstitutionView.as_view(),name="institutions")
]
