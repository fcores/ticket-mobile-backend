"""
Custom exception handlers and error responses.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.conf import settings


def custom_exception_handler(exc, context):
    """
    Custom exception handler for normalized error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Normalize error response
        error_response = {
            'error': get_error_message(exc),
            'details': response.data if isinstance(response.data, dict) else {'message': str(response.data)},
            'timestamp': timezone.now().isoformat(),
            'status_code': response.status_code
        }
        
        response.data = error_response
    else:
        # Handle unhandled exceptions (500 errors)
        # This ensures all errors return JSON instead of HTML
        import traceback
        import logging
        
        logger = logging.getLogger(__name__)
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        error_response = {
            'error': 'Error interno del servidor',
            'details': {
                'message': str(exc) if settings.DEBUG else 'Ha ocurrido un error inesperado'
            },
            'timestamp': timezone.now().isoformat(),
            'status_code': 500
        }
        
        if settings.DEBUG:
            error_response['details']['traceback'] = traceback.format_exc()
        
        response = Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response


def get_error_message(exc):
    """
    Get a user-friendly error message based on exception type.
    """
    error_messages = {
        'NotAuthenticated': 'Debe iniciar sesión para acceder a este recurso',
        'AuthenticationFailed': 'Credenciales de autenticación inválidas',
        'PermissionDenied': 'No tiene permiso para realizar esta acción',
        'NotFound': 'El recurso solicitado no existe',
        'MethodNotAllowed': 'Método HTTP no permitido',
        'ValidationError': 'Los datos proporcionados son inválidos',
        'ParseError': 'Error al procesar los datos enviados',
        'Throttled': 'Demasiadas solicitudes. Por favor, intente más tarde',
    }
    
    exc_class = exc.__class__.__name__
    return error_messages.get(exc_class, 'Ha ocurrido un error en el servidor')


class BadRequestError(Exception):
    """Custom exception for bad requests."""
    def __init__(self, message, details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class UnauthorizedError(Exception):
    """Custom exception for unauthorized access."""
    def __init__(self, message="No autorizado"):
        self.message = message
        super().__init__(self.message)


class ForbiddenError(Exception):
    """Custom exception for forbidden access."""
    def __init__(self, message="Acceso prohibido"):
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    """Custom exception for not found resources."""
    def __init__(self, message="Recurso no encontrado"):
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    """Custom exception for conflict errors."""
    def __init__(self, message="Conflicto al procesar la solicitud"):
        self.message = message
        super().__init__(self.message)

