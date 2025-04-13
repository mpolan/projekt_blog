from django.urls import path
from django.contrib.auth import views as auth_views  # Dodaj import widoku logowania
from .views import SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
]