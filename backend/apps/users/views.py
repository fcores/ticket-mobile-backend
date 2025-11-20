"""
Views for users app.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import User
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    UserRoleUpdateSerializer,
    UserActivationSerializer
)
from .permissions import IsAdminUser


class UserPagination(PageNumberPagination):
    """Custom pagination for users list."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users_view(request):
    """
    List all users (any authenticated user can view).
    GET /api/users/
    
    Query params:
    - page: page number
    - page_size: items per page
    - role: filter by role
    - is_active: filter by active status
    - search: search by name or email
    """
    queryset = User.objects.all().order_by('-created_at')
    
    # Filters
    role = request.query_params.get('role')
    is_active = request.query_params.get('is_active')
    search = request.query_params.get('search')
    
    if role:
        queryset = queryset.filter(role=role)
    
    if is_active is not None:
        is_active_bool = is_active.lower() == 'true'
        queryset = queryset.filter(is_active=is_active_bool)
    
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Pagination
    paginator = UserPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    serializer = UserListSerializer(paginated_queryset, many=True)
    
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_support_users_view(request):
    """
    Get list of support users (for ticket assignment).
    GET /api/users/support/
    """
    support_users = User.objects.filter(role='support', is_active=True).order_by('first_name', 'last_name')
    serializer = UserListSerializer(support_users, many=True)
    return Response({
        'count': support_users.count(),
        'results': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile_view(request):
    """
    Get current user profile.
    GET /api/users/profile/
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile_view(request):
    """
    Update current user profile.
    PUT/PATCH /api/users/profile/
    """
    user = request.user
    serializer = UserUpdateSerializer(
        user,
        data=request.data,
        partial=request.method == 'PATCH'
    )
    
    if serializer.is_valid():
        serializer.save()
        
        # Return updated user data
        user_data = UserSerializer(user).data
        
        return Response({
            'msg': 'Perfil actualizado exitosamente',
            'user': user_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al actualizar perfil',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_user_detail_view(request, user_id):
    """
    Get user details by ID (admin only).
    GET /api/users/{id}/
    """
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_user_role_view(request, user_id):
    """
    Update user role (admin only).
    PUT/PATCH /api/users/{id}/role/
    """
    user = get_object_or_404(User, id=user_id)
    
    # Prevent admin from changing their own role
    if user.id == request.user.id:
        return Response({
            'error': 'No puedes cambiar tu propio rol'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = UserRoleUpdateSerializer(user, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
        user_data = UserSerializer(user).data
        
        return Response({
            'msg': 'Rol actualizado exitosamente',
            'user': user_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al actualizar rol',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def toggle_user_activation_view(request, user_id):
    """
    Activate or deactivate user (admin only).
    PATCH /api/users/{id}/activation/
    """
    user = get_object_or_404(User, id=user_id)
    
    # Prevent admin from deactivating themselves
    if user.id == request.user.id:
        return Response({
            'error': 'No puedes desactivar tu propia cuenta'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = UserActivationSerializer(user, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
        user_data = UserSerializer(user).data
        
        action = 'activado' if user.is_active else 'desactivado'
        
        return Response({
            'msg': f'Usuario {action} exitosamente',
            'user': user_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al cambiar estado del usuario',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_user_view(request, user_id):
    """
    Delete user (admin only).
    DELETE /api/users/{id}/
    """
    user = get_object_or_404(User, id=user_id)
    
    # Prevent admin from deleting themselves
    if user.id == request.user.id:
        return Response({
            'error': 'No puedes eliminar tu propia cuenta'
        }, status=status.HTTP_403_FORBIDDEN)
    
    user_email = user.email
    user.delete()
    
    return Response({
        'msg': f'Usuario {user_email} eliminado exitosamente'
    }, status=status.HTTP_200_OK)

