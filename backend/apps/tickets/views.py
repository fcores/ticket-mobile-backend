"""
Views for tickets app.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Ticket
from .serializers import (
    TicketListSerializer,
    TicketDetailSerializer,
    TicketCreateSerializer,
    TicketUpdateSerializer,
    TicketStatusUpdateSerializer,
    TicketAssignSerializer
)
from apps.users.permissions import IsAdminUser, IsSupportOrAdmin


class TicketPagination(PageNumberPagination):
    """Custom pagination for tickets list."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tickets_view(request):
    """
    List tickets based on user role.
    GET /api/tickets/
    
    Query params:
    - status: filter by status
    - priority: filter by priority
    - page: page number
    - page_size: items per page
    - search: search in title and description
    """
    user = request.user
    
    # Filter based on user role
    if user.role == 'sysAdmin':
        # Admin can see all tickets
        queryset = Ticket.objects.all()
    elif user.role == 'support':
        # Support can see assigned tickets and unassigned tickets
        queryset = Ticket.objects.filter(
            Q(assignee=user) | Q(assignee__isnull=True)
        )
    else:
        # Regular users can only see their own tickets
        queryset = Ticket.objects.filter(creator=user)
    
    # Apply filters
    status_filter = request.query_params.get('status')
    priority_filter = request.query_params.get('priority')
    search = request.query_params.get('search')
    
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    if priority_filter:
        queryset = queryset.filter(priority=priority_filter)
    
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Order by most recent
    queryset = queryset.order_by('-created_at')
    
    # Pagination
    paginator = TicketPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    serializer = TicketListSerializer(paginated_queryset, many=True)
    
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ticket_view(request):
    """
    Create a new ticket.
    POST /api/tickets/
    """
    serializer = TicketCreateSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        ticket = serializer.save()
        
        # Auto-asignar a un usuario de soporte aleatorio
        from apps.users.models import User
        import random
        soportes = User.objects.filter(role='support', is_active=True)
        if soportes.exists():
            ticket.assignee = random.choice(soportes)
            ticket.save()
        
        # Return detailed ticket data
        ticket_data = TicketDetailSerializer(ticket).data
        
        return Response({
            'msg': 'Ticket creado exitosamente',
            'ticket': ticket_data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Error al crear ticket',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ticket_detail_view(request, ticket_id):
    """
    Get ticket details.
    GET /api/tickets/{id}/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user = request.user
    
    # Check permissions
    if user.role not in ['sysAdmin', 'support']:
        # Regular users can only see their own tickets
        if ticket.creator != user:
            return Response({
                'error': 'No tienes permiso para ver este ticket'
            }, status=status.HTTP_403_FORBIDDEN)
    elif user.role == 'support':
        # Support can only see assigned tickets or unassigned tickets
        if ticket.assignee and ticket.assignee != user:
            return Response({
                'error': 'No tienes permiso para ver este ticket'
            }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = TicketDetailSerializer(ticket)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_ticket_view(request, ticket_id):
    """
    Update ticket.
    PUT/PATCH /api/tickets/{id}/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user = request.user
    
    # Check permissions
    can_update = False
    
    if user.role == 'sysAdmin':
        can_update = True
    elif user.role == 'support' and (ticket.assignee == user or not ticket.assignee):
        can_update = True
    elif ticket.creator == user and ticket.status == 'open':
        # Creator can only update open tickets (limited fields)
        can_update = True
    
    if not can_update:
        return Response({
            'error': 'No tienes permiso para actualizar este ticket'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = TicketUpdateSerializer(
        ticket,
        data=request.data,
        partial=request.method == 'PATCH',
        context={'request': request}
    )
    
    if serializer.is_valid():
        # Regular users can't change status or assignee
        if user.role not in ['support', 'sysAdmin']:
            if 'status' in serializer.validated_data:
                return Response({
                    'error': 'No tienes permiso para cambiar el estado del ticket'
                }, status=status.HTTP_403_FORBIDDEN)
            if 'assignee_id' in serializer.validated_data:
                return Response({
                    'error': 'No tienes permiso para asignar tickets'
                }, status=status.HTTP_403_FORBIDDEN)
        
        serializer.save()
        
        # Return updated ticket
        ticket_data = TicketDetailSerializer(ticket).data
        
        return Response({
            'msg': 'Ticket actualizado exitosamente',
            'ticket': ticket_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al actualizar ticket',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsSupportOrAdmin])
def update_ticket_status_view(request, ticket_id):
    """
    Update only ticket status (support/admin only).
    PATCH /api/tickets/{id}/status/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user = request.user
    
    # Support can only update their assigned tickets
    if user.role == 'support' and ticket.assignee != user:
        return Response({
            'error': 'Solo puedes actualizar el estado de tus tickets asignados'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = TicketStatusUpdateSerializer(ticket, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
        ticket_data = TicketDetailSerializer(ticket).data
        
        return Response({
            'msg': 'Estado actualizado exitosamente',
            'ticket': ticket_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al actualizar estado',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsSupportOrAdmin])
def assign_ticket_view(request, ticket_id):
    """
    Assign ticket to user (support/admin only).
    PATCH /api/tickets/{id}/assign/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    serializer = TicketAssignSerializer(data=request.data)
    
    if serializer.is_valid():
        ticket.assignee_id = serializer.validated_data['assigneeId']
        ticket.save()
        
        ticket_data = TicketDetailSerializer(ticket).data
        
        assignee_name = ticket.assignee.full_name if ticket.assignee else 'nadie'
        
        return Response({
            'msg': f'Ticket asignado a {assignee_name} exitosamente',
            'ticket': ticket_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al asignar ticket',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_ticket_view(request, ticket_id):
    """
    Delete ticket (admin only).
    DELETE /api/tickets/{id}/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket_title = ticket.title
    ticket.delete()
    
    return Response({
        'msg': f'Ticket "{ticket_title}" eliminado exitosamente'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tickets_view(request):
    """
    Get current user's tickets.
    GET /api/tickets/my-tickets/
    """
    user = request.user
    queryset = Ticket.objects.filter(creator=user).order_by('-created_at')
    
    # Apply filters
    status_filter = request.query_params.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    # Pagination
    paginator = TicketPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    serializer = TicketListSerializer(paginated_queryset, many=True)
    
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSupportOrAdmin])
def assigned_tickets_view(request):
    """
    Get tickets assigned to current user (support/admin).
    GET /api/tickets/assigned/
    """
    user = request.user
    queryset = Ticket.objects.filter(assignee=user).order_by('-created_at')
    
    # Apply filters
    status_filter = request.query_params.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    # Pagination
    paginator = TicketPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    serializer = TicketListSerializer(paginated_queryset, many=True)
    
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSupportOrAdmin])
def unassigned_tickets_view(request):
    """
    Get unassigned tickets (support/admin).
    GET /api/tickets/unassigned/
    """
    queryset = Ticket.objects.filter(assignee__isnull=True).order_by('-created_at')
    
    # Pagination
    paginator = TicketPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    serializer = TicketListSerializer(paginated_queryset, many=True)
    
    return paginator.get_paginated_response(serializer.data)

