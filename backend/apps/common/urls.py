"""
URL configuration for common app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # System endpoints
    path('health/', views.health_check_view, name='health-check'),
    path('info/', views.api_info_view, name='api-info'),
    path('version/', views.api_version_view, name='api-version'),
]

