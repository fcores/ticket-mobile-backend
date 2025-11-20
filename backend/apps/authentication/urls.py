"""
URL configuration for authentication app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register_view, name='auth-register'),
    path('auth/login/', views.login_view, name='auth-login'),
    path('auth/refresh/', views.refresh_token_view, name='auth-refresh'),
    path('auth/logout/', views.logout_view, name='auth-logout'),
    path('auth/me/', views.me_view, name='auth-me'),
    path('auth/change-password/', views.change_password_view, name='auth-change-password'),
    path('auth/password-reset/', views.password_reset_request_view, name='auth-password-reset'),
]

