"""
Views for attachments app.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Attachment
from .serializers import AttachmentSerializer, AttachmentUploadSerializer
from apps.tickets.models import Ticket


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_ticket_attachments_view(request, ticket_id):
    """
    List all attachments for a ticket.
    GET /api/tickets/{ticket_id}/attachments/
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
    
    # Get attachments
    attachments = ticket.attachments.all()
    
    # Filter private attachments for regular users
    if user.role not in ['support', 'sysAdmin']:
        attachments = attachments.filter(is_private=False)
    
    serializer = AttachmentSerializer(
        attachments,
        many=True,
        context={'request': request}
    )
    
    return Response({
        'count': attachments.count(),
        'attachments': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_attachment_view(request, ticket_id):
    """
    Upload an attachment to a ticket.
    POST /api/tickets/{ticket_id}/attachments/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user = request.user
    
    # Check if user can upload to this ticket
    can_upload = False
    
    if user.role == 'sysAdmin':
        can_upload = True
    elif user.role == 'support' and (ticket.assignee == user or not ticket.assignee):
        can_upload = True
    elif ticket.creator == user:
        can_upload = True
    
    if not can_upload:
        return Response({
            'error': 'No tienes permiso para subir archivos a este ticket'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = AttachmentUploadSerializer(
        data=request.data,
        context={'request': request, 'ticket': ticket}
    )
    
    if serializer.is_valid():
        try:
            attachment = serializer.save()
            
            attachment_data = AttachmentSerializer(
                attachment,
                context={'request': request}
            ).data
            
            return Response({
                'msg': 'Archivo subido exitosamente',
                'attachment': attachment_data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'error': 'Error al subir archivo',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'error': 'Error al subir archivo',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attachment_detail_view(request, ticket_id, attachment_id):
    """
    Get attachment details.
    GET /api/tickets/{ticket_id}/attachments/{attachment_id}/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    attachment = get_object_or_404(Attachment, id=attachment_id, ticket=ticket)
    user = request.user
    
    # Check permissions for private attachments
    if attachment.is_private and user.role not in ['support', 'sysAdmin']:
        return Response({
            'error': 'No tienes permiso para ver este archivo'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = AttachmentSerializer(attachment, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_attachment_view(request, ticket_id, attachment_id):
    """
    Delete an attachment.
    DELETE /api/tickets/{ticket_id}/attachments/{attachment_id}/
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    attachment = get_object_or_404(Attachment, id=attachment_id, ticket=ticket)
    user = request.user
    
    # Only uploader or admin can delete
    if attachment.uploaded_by != user and user.role != 'sysAdmin':
        return Response({
            'error': 'Solo quien subió el archivo o un administrador puede eliminarlo'
        }, status=status.HTTP_403_FORBIDDEN)
    
    filename = attachment.original_filename
    
    # Delete the file from storage
    if attachment.file:
        try:
            attachment.file.delete()
        except Exception:
            pass  # Continue even if file deletion fails
    
    attachment.delete()
    
    return Response({
        'msg': f'Archivo "{filename}" eliminado exitosamente'
    }, status=status.HTTP_200_OK)

