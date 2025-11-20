"""
Views for categories app.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Category
from .serializers import (
    CategorySerializer,
    CategoryCreateSerializer,
    CategoryUpdateSerializer
)
from apps.users.permissions import IsAdminUser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_categories_view(request):
    """
    List all categories.
    GET /api/categories/
    """
    categories = Category.objects.all().order_by('name')
    
    # Optional search filter
    search = request.query_params.get('search')
    if search:
        categories = categories.filter(name__icontains=search)
    
    serializer = CategorySerializer(categories, many=True)
    
    return Response({
        'count': categories.count(),
        'categories': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_category_view(request):
    """
    Create a new category (admin only).
    POST /api/categories/
    """
    serializer = CategoryCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        category = serializer.save()
        
        category_data = CategorySerializer(category).data
        
        return Response({
            'msg': 'Categoría creada exitosamente',
            'category': category_data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Error al crear categoría',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category_detail_view(request, category_id):
    """
    Get category details.
    GET /api/categories/{id}/
    """
    category = get_object_or_404(Category, id=category_id)
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_category_view(request, category_id):
    """
    Update category (admin only).
    PUT/PATCH /api/categories/{id}/
    """
    category = get_object_or_404(Category, id=category_id)
    
    serializer = CategoryUpdateSerializer(
        category,
        data=request.data,
        partial=request.method == 'PATCH'
    )
    
    if serializer.is_valid():
        serializer.save()
        
        category_data = CategorySerializer(category).data
        
        return Response({
            'msg': 'Categoría actualizada exitosamente',
            'category': category_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al actualizar categoría',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_category_view(request, category_id):
    """
    Delete category (admin only).
    DELETE /api/categories/{id}/
    """
    category = get_object_or_404(Category, id=category_id)
    
    # Check if category has tickets
    if hasattr(category, 'tickets') and category.tickets.exists():
        return Response({
            'error': 'No se puede eliminar una categoría que tiene tickets asociados',
            'ticketCount': category.tickets.count()
        }, status=status.HTTP_400_BAD_REQUEST)
    
    category_name = category.name
    category.delete()
    
    return Response({
        'msg': f'Categoría "{category_name}" eliminada exitosamente'
    }, status=status.HTTP_200_OK)

