from django.urls import path 
from InstitutionClasses.views import InstitutionClassView
urlpatterns=[
    path("classes",InstitutionClassView.as_view(),name="institution_classes")

    ]