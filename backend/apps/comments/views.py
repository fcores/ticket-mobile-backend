"""
Views for comments app.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Comment
from .serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer
)
from apps.tickets.models import Ticket


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_ticket_comments_view(request, ticket_id):
    """
    List all comments for a ticket.
    GET /api/tickets/{ticket_id}/comments/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user = request.user
    
    # Check if user can view this ticket
    can_view = False
    
    if user.role == 'sysAdmin':
        can_view = True
    elif user.role == 'support' and (ticket.assignee == user or not ticket.assignee):
        can_view = True
    elif ticket.creator == user:
        can_view = True
    
    if not can_view:
        return Response({
            'error': 'No tienes permiso para ver este ticket'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Get comments
    comments = ticket.comments.all()
    
    # Filter private comments for regular users
    if user.role not in ['support', 'sysAdmin']:
        comments = comments.filter(is_private=False)
    
    serializer = CommentSerializer(comments, many=True)
    
    return Response({
        'count': comments.count(),
        'comments': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment_view(request, ticket_id):
    """
    Create a comment on a ticket.
    POST /api/tickets/{ticket_id}/comments/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user = request.user
    
    # Check if user can comment on this ticket
    can_comment = False
    
    if user.role == 'sysAdmin':
        can_comment = True
    elif user.role == 'support' and (ticket.assignee == user or not ticket.assignee):
        can_comment = True
    elif ticket.creator == user:
        can_comment = True
    
    if not can_comment:
        return Response({
            'error': 'No tienes permiso para comentar en este ticket'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CommentCreateSerializer(
        data=request.data,
        context={'request': request, 'ticket': ticket}
    )
    
    if serializer.is_valid():
        comment = serializer.save()
        
        comment_data = CommentSerializer(comment).data
        
        return Response({
            'msg': 'Comentario creado exitosamente',
            'comment': comment_data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Error al crear comentario',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comment_detail_view(request, ticket_id, comment_id):
    """
    Get comment details.
    GET /api/tickets/{ticket_id}/comments/{comment_id}/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    comment = get_object_or_404(Comment, id=comment_id, ticket=ticket)
    user = request.user
    
    # Check permissions
    if comment.is_private and user.role not in ['support', 'sysAdmin']:
        return Response({
            'error': 'No tienes permiso para ver este comentario'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_comment_view(request, ticket_id, comment_id):
    """
    Update a comment.
    PUT/PATCH /api/tickets/{ticket_id}/comments/{comment_id}/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    comment = get_object_or_404(Comment, id=comment_id, ticket=ticket)
    user = request.user
    
    # Only author or admin can update
    if comment.author != user and user.role != 'sysAdmin':
        return Response({
            'error': 'Solo el autor o un administrador puede editar este comentario'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CommentUpdateSerializer(
        comment,
        data=request.data,
        partial=request.method == 'PATCH'
    )
    
    if serializer.is_valid():
        serializer.save()
        
        comment_data = CommentSerializer(comment).data
        
        return Response({
            'msg': 'Comentario actualizado exitosamente',
            'comment': comment_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al actualizar comentario',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment_view(request, ticket_id, comment_id):
    """
    Delete a comment.
    DELETE /api/tickets/{ticket_id}/comments/{comment_id}/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    comment = get_object_or_404(Comment, id=comment_id, ticket=ticket)
    user = request.user
    
    # Only author or admin can delete
    if comment.author != user and user.role != 'sysAdmin':
        return Response({
            'error': 'Solo el autor o un administrador puede eliminar este comentario'
        }, status=status.HTTP_403_FORBIDDEN)
    
    comment.delete()
    
    return Response({
        'msg': 'Comentario eliminado exitosamente'
    }, status=status.HTTP_200_OK)

