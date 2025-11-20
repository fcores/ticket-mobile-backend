"""
Views for common app.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.db import connection
from django.conf import settings

from .serializers import HealthCheckSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_view(request):
    """
    Health check endpoint for monitoring.
    GET /api/health/
    """
    # Check database connection
    db_status = 'healthy'
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    # Check various services
    services = {
        'database': db_status,
        'api': 'healthy',
    }
    
    # Determine overall status
    overall_status = 'healthy' if db_status == 'healthy' else 'unhealthy'
    
    health_data = {
        'status': overall_status,
        'message': 'Sistema de tickets funcionando correctamente' if overall_status == 'healthy' else 'Sistema con problemas',
        'timestamp': timezone.now(),
        'version': '1.0.0',
        'database': db_status,
        'services': services
    }
    
    serializer = HealthCheckSerializer(data=health_data)
    
    if serializer.is_valid():
        response_status = status.HTTP_200_OK if overall_status == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(serializer.validated_data, status=response_status)
    
    return Response({
        'status': 'error',
        'message': 'Error al verificar el estado del sistema'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info_view(request):
    """
    Get API information.
    GET /api/info/
    """
    info = {
        'name': 'Sistema de Tickets API',
        'version': '1.0.0',
        'description': 'API REST para sistema de gestión de tickets de soporte',
        'documentation': {
            'swagger': f"{request.build_absolute_uri('/api/schema/swagger-ui/')}",
            'redoc': f"{request.build_absolute_uri('/api/schema/redoc/')}"
        },
        'endpoints': {
            'authentication': '/api/auth/',
            'users': '/api/users/',
            'tickets': '/api/tickets/',
            'comments': '/api/tickets/{id}/comments/',
            'attachments': '/api/tickets/{id}/attachments/',
            'categories': '/api/categories/',
            'metrics': '/api/metrics/',
            'health': '/api/health/'
        },
        'contact': {
            'team': 'Equipo de Desarrollo',
            'productOwner': 'Lautaro Cavallo'
        }
    }
    
    return Response(info, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_version_view(request):
    """
    Get API version.
    GET /api/version/
    """
    return Response({
        'version': '1.0.0',
        'releaseDate': '2024-01-01',
        'environment': 'development' if settings.DEBUG else 'production'
    }, status=status.HTTP_200_OK)

