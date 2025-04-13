from django.urls import path
from django.contrib.auth import views as auth_views  # Dodaj import widoku logowania
from .views import SignUpView, account_settings
from . import views


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path('edit/', views.edit_profile, name='edit_profile'),  # Edytowanie profilu
    path('settings/', views.account_settings, name='account_settings'),  # Ustawienia konta
]