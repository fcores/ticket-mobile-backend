"""
URL configuration for users app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # User profile endpoints
    path('users/profile/', views.get_user_profile_view, name='user-profile'),
    path('users/profile/update/', views.update_user_profile_view, name='user-profile-update'),
    
    # Support users endpoint (for ticket assignment)
    path('users/support/', views.get_support_users_view, name='support-users-list'),
    
    # Admin user management endpoints
    path('users/', views.list_users_view, name='users-list'),
    path('users/<int:user_id>/', views.get_user_detail_view, name='user-detail'),
    path('users/<int:user_id>/role/', views.update_user_role_view, name='user-role-update'),
    path('users/<int:user_id>/activation/', views.toggle_user_activation_view, name='user-activation'),
    path('users/<int:user_id>/delete/', views.delete_user_view, name='user-delete'),
]

