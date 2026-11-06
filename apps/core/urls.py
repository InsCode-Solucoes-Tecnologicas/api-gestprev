from django.urls import path

from . import views

urlpatterns = [
    path("saude/", views.SaudeView.as_view(), name="saude"),
    path("auth/csrf/", views.CsrfView.as_view(), name="auth-csrf"),
    path("auth/login/", views.LoginView.as_view(), name="auth-login"),
    path("auth/logout/", views.LogoutView.as_view(), name="auth-logout"),
    path("auth/eu/", views.EuView.as_view(), name="auth-eu"),
]
