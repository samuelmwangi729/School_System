from django.urls import path 
from .views import subjectsView

urlpatterns=[
        path("subjects",subjectsView.as_view(),name="subjects")
    ]