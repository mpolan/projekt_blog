from django.urls import path
from .views import SignUpView, account_settings, custom_login_view
from . import views


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", custom_login_view, name="login"),
    path('edit/', views.edit_profile, name='edit_profile'),  # Edytowanie profilu
    path('settings/', views.account_settings, name='account_settings'),  # Ustawienia konta
]