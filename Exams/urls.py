from django.urls import path 
from Exams.views import ExaminationView
urlpatterns=[
    path("exams",ExaminationView.as_view(),name="examinations"),
    path("exam/<str:exam_name>",ExaminationView.as_view(),name="exam_update"),
    ]