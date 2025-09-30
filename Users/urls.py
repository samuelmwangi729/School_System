from django.urls import path 
from Users.views import LoginView, UserView
urlpatterns = [
    path("register",UserView.as_view(),name="register"),
    path("login",LoginView.as_view(),name="login"),
    path("update",UserView.as_view(),name="update_user"),
]
