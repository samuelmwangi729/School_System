from django.urls import path 
from Users.views import UserView
urlpatterns = [
    path("register",UserView.as_view(),name="register")
]
