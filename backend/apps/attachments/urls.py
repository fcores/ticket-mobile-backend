"""
URL configuration for attachments app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Attachments for a ticket
    path('tickets/<int:ticket_id>/attachments/', views.list_ticket_attachments_view, name='ticket-attachments-list'),
    path('tickets/<int:ticket_id>/attachments/upload/', views.upload_attachment_view, name='ticket-attachments-upload'),
    path('tickets/<int:ticket_id>/attachments/<int:attachment_id>/', views.get_attachment_detail_view, name='attachment-detail'),
    path('tickets/<int:ticket_id>/attachments/<int:attachment_id>/delete/', views.delete_attachment_view, name='attachment-delete'),
]

