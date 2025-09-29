from django.urls import path 
from Teachers.views import TeacherGenericView

urlpatterns=[
    path("teachers",TeacherGenericView.as_view(),name="teachers")
    ]