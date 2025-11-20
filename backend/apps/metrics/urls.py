"""
URL configuration for metrics app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Metrics endpoints
    path('metrics/tickets/overview/', views.tickets_overview_view, name='metrics-tickets-overview'),
    path('metrics/tickets/performance/', views.tickets_performance_view, name='metrics-tickets-performance'),
    path('metrics/users/activity/', views.users_activity_view, name='metrics-users-activity'),
    path('metrics/system/health/', views.system_health_view, name='metrics-system-health'),
]

