from django.urls import path 
from Institutions.views import InstitutionView
urlpatterns = [
    path("institutions",InstitutionView.as_view(),name="institutions"),
    path("institution/<str:institution_name>",InstitutionView.as_view(),name="institution_update"),
]
