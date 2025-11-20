"""
Views for authentication app.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash

from apps.users.serializers import UserSerializer
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    TokenRefreshSerializer
)


def get_tokens_for_user(user):
    """Generate JWT tokens for user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user.
    POST /api/auth/register/
    """
    serializer = UserRegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            user = serializer.save()
            user.last_login = timezone.now()
            user.save()
            
            # Generate tokens
            tokens = get_tokens_for_user(user)
            
            # Serialize user data
            user_data = UserSerializer(user).data
            
            return Response({
                'msg': 'Usuario registrado exitosamente',
                'user': user_data,
                'accessToken': tokens['access'],
                'refreshToken': tokens['refresh']
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'error': 'Error al crear el usuario',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'error': 'Datos inválidos',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login user and return JWT tokens.
    POST /api/auth/login/
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Generate tokens
        tokens = get_tokens_for_user(user)
        
        # Serialize user data
        user_data = UserSerializer(user).data
        
        return Response({
            'accessToken': tokens['access'],
            'refreshToken': tokens['refresh'],
            'user': user_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Credenciales inválidas',
        'details': serializer.errors
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """
    Refresh access token using refresh token.
    POST /api/auth/refresh/
    """
    serializer = TokenRefreshSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'error': 'Refresh token requerido',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        refresh_token = RefreshToken(serializer.validated_data['refreshToken'])
        
        return Response({
            'accessToken': str(refresh_token.access_token)
        }, status=status.HTTP_200_OK)
    
    except TokenError as e:
        return Response({
            'error': 'Token inválido o expirado',
            'detail': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    except Exception as e:
        return Response({
            'error': 'Error al renovar token',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout user by blacklisting refresh token.
    POST /api/auth/logout/
    """
    try:
        refresh_token = request.data.get('refreshToken')
        
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'msg': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
    
    except TokenError:
        return Response({
            'error': 'Token inválido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        # Even if token blacklisting fails, we can still logout
        return Response({
            'msg': 'Logout exitoso'
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Get current authenticated user information.
    GET /api/auth/me/
    """
    user = request.user
    serializer = UserSerializer(user)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Change user password.
    POST /api/auth/change-password/
    """
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['newPassword'])
        user.save()
        
        # Keep user logged in after password change
        update_session_auth_hash(request, user)
        
        return Response({
            'msg': 'Contraseña actualizada exitosamente'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Error al cambiar contraseña',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request_view(request):
    """
    Request password reset email.
    POST /api/auth/password-reset/
    """
    serializer = PasswordResetRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        # TODO: Implement email sending logic
        # For security, always return success even if email doesn't exist
        
        return Response({
            'msg': 'Si el email existe, recibirás instrucciones para restablecer tu contraseña'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Email inválido',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

