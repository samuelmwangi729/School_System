from django.urls import path 
from .views import subjectsView

urlpatterns=[
        path("subjects",subjectsView.as_view(),name="subjects"),
        path("subject/<int:subject_code>",subjectsView.as_view(),name="update_subject"),
    ]