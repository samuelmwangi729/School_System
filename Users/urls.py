from django.urls import path 
from Users.views import JwtTokenObtainView, UserUpdateView, UserView,StudentsView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [
    path("register",UserView.as_view(),name="register"),
    path("students",StudentsView.as_view(),name="students"),
    path("login",JwtTokenObtainView.as_view(), name='token'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path("update",UserUpdateView.as_view(),name="update_user"),
]
