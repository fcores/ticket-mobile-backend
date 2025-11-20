"""
Views for metrics app.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

from apps.users.models import User
from apps.tickets.models import Ticket
from apps.comments.models import Comment
from apps.users.permissions import IsAdminUser, IsSupportOrAdmin
from .serializers import (
    TicketMetricsSerializer,
    TicketPriorityMetricsSerializer,
    TicketPerformanceSerializer,
    UserActivitySerializer,
    SystemHealthSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSupportOrAdmin])
def tickets_overview_view(request):
    """
    Get overview of tickets metrics.
    GET /api/metrics/tickets/overview/
    """
    # Count tickets by status
    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.filter(status='open').count()
    in_progress_tickets = Ticket.objects.filter(status='in_progress').count()
    resolved_tickets = Ticket.objects.filter(status='resolved').count()
    closed_tickets = Ticket.objects.filter(status='closed').count()
    canceled_tickets = Ticket.objects.filter(status='canceled').count()
    unassigned_tickets = Ticket.objects.filter(assignee__isnull=True).count()
    
    # Count by priority
    priority_metrics = {
        'low': Ticket.objects.filter(priority='low').count(),
        'medium': Ticket.objects.filter(priority='medium').count(),
        'high': Ticket.objects.filter(priority='high').count(),
        'urgent': Ticket.objects.filter(priority='urgent').count(),
    }
    
    metrics_data = {
        'total': total_tickets,
        'open': open_tickets,
        'inProgress': in_progress_tickets,
        'resolved': resolved_tickets,
        'closed': closed_tickets,
        'canceled': canceled_tickets,
        'unassigned': unassigned_tickets
    }
    
    status_serializer = TicketMetricsSerializer(data=metrics_data)
    priority_serializer = TicketPriorityMetricsSerializer(data=priority_metrics)
    
    if status_serializer.is_valid() and priority_serializer.is_valid():
        return Response({
            'statusMetrics': status_serializer.validated_data,
            'priorityMetrics': priority_serializer.validated_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al obtener métricas'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSupportOrAdmin])
def tickets_performance_view(request):
    """
    Get ticket performance metrics.
    GET /api/metrics/tickets/performance/
    """
    # Calculate average resolution time
    resolved_tickets = Ticket.objects.filter(
        status='resolved',
        resolved_at__isnull=False
    )
    
    total_resolved = resolved_tickets.count()
    
    avg_resolution_time = 0
    if total_resolved > 0:
        total_hours = 0
        for ticket in resolved_tickets:
            delta = ticket.resolved_at - ticket.created_at
            total_hours += delta.total_seconds() / 3600
        avg_resolution_time = total_hours / total_resolved
    
    # Count tickets created in time periods
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = now - timedelta(days=7)
    month_start = now - timedelta(days=30)
    
    created_today = Ticket.objects.filter(created_at__gte=today_start).count()
    created_this_week = Ticket.objects.filter(created_at__gte=week_start).count()
    created_this_month = Ticket.objects.filter(created_at__gte=month_start).count()
    
    # Calculate resolution rate
    total_tickets = Ticket.objects.count()
    resolution_rate = (total_resolved / total_tickets * 100) if total_tickets > 0 else 0
    
    performance_data = {
        'averageResolutionTime': round(avg_resolution_time, 2),
        'totalResolved': total_resolved,
        'totalCreatedToday': created_today,
        'totalCreatedThisWeek': created_this_week,
        'totalCreatedThisMonth': created_this_month,
        'resolutionRate': round(resolution_rate, 2)
    }
    
    serializer = TicketPerformanceSerializer(data=performance_data)
    
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al obtener métricas de rendimiento'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def users_activity_view(request):
    """
    Get user activity metrics (admin only).
    GET /api/metrics/users/activity/
    """
    users = User.objects.filter(is_active=True)
    
    activity_data = []
    
    for user in users:
        tickets_created = Ticket.objects.filter(creator=user).count()
        tickets_assigned = Ticket.objects.filter(assignee=user).count()
        tickets_resolved = Ticket.objects.filter(
            assignee=user,
            status='resolved'
        ).count()
        comments_posted = Comment.objects.filter(author=user).count()
        
        # Determine last activity
        last_activity = user.last_login or user.created_at
        
        # Check for recent ticket or comment activity
        last_ticket = Ticket.objects.filter(creator=user).order_by('-created_at').first()
        last_comment = Comment.objects.filter(author=user).order_by('-created_at').first()
        
        if last_ticket and last_ticket.created_at > last_activity:
            last_activity = last_ticket.created_at
        if last_comment and last_comment.created_at > last_activity:
            last_activity = last_comment.created_at
        
        activity_data.append({
            'userId': user.id,
            'userName': user.full_name,
            'email': user.email,
            'role': user.role,
            'ticketsCreated': tickets_created,
            'ticketsAssigned': tickets_assigned,
            'ticketsResolved': tickets_resolved,
            'commentsPosted': comments_posted,
            'lastActivity': last_activity
        })
    
    # Sort by last activity
    activity_data.sort(key=lambda x: x['lastActivity'], reverse=True)
    
    serializer = UserActivitySerializer(data=activity_data, many=True)
    
    if serializer.is_valid():
        return Response({
            'count': len(activity_data),
            'users': serializer.validated_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al obtener actividad de usuarios'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSupportOrAdmin])
def system_health_view(request):
    """
    Get system health metrics.
    GET /api/metrics/system/health/
    """
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.filter(status='open').count()
    urgent_tickets = Ticket.objects.filter(priority='urgent').count()
    unassigned_tickets = Ticket.objects.filter(assignee__isnull=True).count()
    
    # Calculate average response time (time to first assignment)
    assigned_tickets = Ticket.objects.filter(assignee__isnull=False)
    total_response_time = 0
    count = 0
    
    for ticket in assigned_tickets:
        # This is a simple approximation
        # In a real system, you'd track assignment history
        delta = ticket.updated_at - ticket.created_at
        total_response_time += delta.total_seconds() / 3600
        count += 1
    
    avg_response_time = (total_response_time / count) if count > 0 else 0
    
    # Determine system status
    system_status = 'healthy'
    if unassigned_tickets > 10:
        system_status = 'warning'
    if urgent_tickets > 5 or unassigned_tickets > 20:
        system_status = 'critical'
    
    health_data = {
        'status': system_status,
        'totalUsers': total_users,
        'activeUsers': active_users,
        'totalTickets': total_tickets,
        'openTickets': open_tickets,
        'urgentTickets': urgent_tickets,
        'unassignedTickets': unassigned_tickets,
        'averageResponseTime': round(avg_response_time, 2)
    }
    
    serializer = SystemHealthSerializer(data=health_data)
    
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al obtener estado del sistema'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

