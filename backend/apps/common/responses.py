"""
Utility functions for normalized API responses.
"""
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


def success_response(message, data=None, status_code=status.HTTP_200_OK):
    """
    Create a standardized success response.
    
    Args:
        message (str): Success message
        data (dict): Optional data to include
        status_code (int): HTTP status code
    
    Returns:
        Response: DRF Response object
    """
    response_data = {
        'success': True,
        'message': message,
        'timestamp': timezone.now().isoformat()
    }
    
    if data is not None:
        response_data['data'] = data
    
    return Response(response_data, status=status_code)


def error_response(error, details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Create a standardized error response.
    
    Args:
        error (str): Error message
        details (dict): Optional error details
        status_code (int): HTTP status code
    
    Returns:
        Response: DRF Response object
    """
    response_data = {
        'success': False,
        'error': error,
        'timestamp': timezone.now().isoformat()
    }
    
    if details is not None:
        response_data['details'] = details
    
    return Response(response_data, status=status_code)


def created_response(message, data=None):
    """
    Create a standardized response for resource creation.
    
    Args:
        message (str): Success message
        data (dict): Created resource data
    
    Returns:
        Response: DRF Response object
    """
    return success_response(message, data, status.HTTP_201_CREATED)


def deleted_response(message):
    """
    Create a standardized response for resource deletion.
    
    Args:
        message (str): Success message
    
    Returns:
        Response: DRF Response object
    """
    return success_response(message, status_code=status.HTTP_200_OK)


def unauthorized_response(message="No autorizado"):
    """
    Create a standardized unauthorized response.
    
    Args:
        message (str): Error message
    
    Returns:
        Response: DRF Response object
    """
    return error_response(message, status_code=status.HTTP_401_UNAUTHORIZED)


def forbidden_response(message="Acceso prohibido"):
    """
    Create a standardized forbidden response.
    
    Args:
        message (str): Error message
    
    Returns:
        Response: DRF Response object
    """
    return error_response(message, status_code=status.HTTP_403_FORBIDDEN)


def not_found_response(message="Recurso no encontrado"):
    """
    Create a standardized not found response.
    
    Args:
        message (str): Error message
    
    Returns:
        Response: DRF Response object
    """
    return error_response(message, status_code=status.HTTP_404_NOT_FOUND)


def validation_error_response(errors):
    """
    Create a standardized validation error response.
    
    Args:
        errors (dict): Validation errors
    
    Returns:
        Response: DRF Response object
    """
    return error_response(
        "Error de validación",
        details=errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


def server_error_response(message="Error interno del servidor"):
    """
    Create a standardized server error response.
    
    Args:
        message (str): Error message
    
    Returns:
        Response: DRF Response object
    """
    return error_response(
        message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

