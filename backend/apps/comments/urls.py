"""
URL configuration for comments app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Comments for a ticket
    path('tickets/<int:ticket_id>/comments/', views.list_ticket_comments_view, name='ticket-comments-list'),
    path('tickets/<int:ticket_id>/comments/create/', views.create_comment_view, name='ticket-comments-create'),
    path('tickets/<int:ticket_id>/comments/<int:comment_id>/', views.get_comment_detail_view, name='comment-detail'),
    path('tickets/<int:ticket_id>/comments/<int:comment_id>/update/', views.update_comment_view, name='comment-update'),
    path('tickets/<int:ticket_id>/comments/<int:comment_id>/delete/', views.delete_comment_view, name='comment-delete'),
]

