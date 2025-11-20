"""
URL configuration for tickets app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # List and create tickets
    path('tickets/', views.list_tickets_view, name='tickets-list'),
    path('tickets/create/', views.create_ticket_view, name='tickets-create'),
    
    # Special ticket lists
    path('tickets/my-tickets/', views.my_tickets_view, name='tickets-my-tickets'),
    path('tickets/assigned/', views.assigned_tickets_view, name='tickets-assigned'),
    path('tickets/unassigned/', views.unassigned_tickets_view, name='tickets-unassigned'),
    
    # Ticket detail and updates
    path('tickets/<int:ticket_id>/', views.get_ticket_detail_view, name='ticket-detail'),
    path('tickets/<int:ticket_id>/update/', views.update_ticket_view, name='ticket-update'),
    path('tickets/<int:ticket_id>/status/', views.update_ticket_status_view, name='ticket-status'),
    path('tickets/<int:ticket_id>/assign/', views.assign_ticket_view, name='ticket-assign'),
    path('tickets/<int:ticket_id>/delete/', views.delete_ticket_view, name='ticket-delete'),
]

