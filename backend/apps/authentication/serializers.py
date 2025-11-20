"""
Serializers for authentication app.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from apps.users.models import User
import re


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    firstName = serializers.CharField(
        source='first_name',
        min_length=2,
        max_length=50,
        required=True
    )
    lastName = serializers.CharField(
        source='last_name',
        min_length=2,
        max_length=50,
        required=True
    )
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    confirmPassword = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email', 'password', 'confirmPassword']

    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(
                "Ya existe un usuario registrado con este email."
            )
        return value.lower()

    def validate_password(self, value):
        """
        Validate password strength.
        Must contain: uppercase, lowercase, numbers, and special characters.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra mayúscula."
            )
        
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra minúscula."
            )
        
        if not re.search(r'\d', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un número."
            )
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un carácter especial."
            )
        
        # Django's built-in password validation
        validate_password(value)
        return value

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs.pop('confirmPassword'):
            raise serializers.ValidationError({
                "confirmPassword": "Las contraseñas no coinciden."
            })
        return attrs

    def create(self, validated_data):
        """Create new user with hashed password."""
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role='user'  # Default role
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Authenticate user credentials."""
        email = attrs.get('email', '').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                "Debe proporcionar email y contraseña."
            )

        # Try to authenticate
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError(
                "Credenciales inválidas. Por favor, verifique su email y contraseña."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Esta cuenta ha sido desactivada."
            )

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    currentPassword = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    newPassword = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    confirmPassword = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate_currentPassword(self, value):
        """Validate current password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "La contraseña actual es incorrecta."
            )
        return value

    def validate_newPassword(self, value):
        """Validate new password strength."""
        if len(value) < 8:
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra mayúscula."
            )
        
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra minúscula."
            )
        
        if not re.search(r'\d', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un número."
            )
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un carácter especial."
            )
        
        validate_password(value)
        return value

    def validate(self, attrs):
        """Validate that new passwords match."""
        if attrs['newPassword'] != attrs['confirmPassword']:
            raise serializers.ValidationError({
                "confirmPassword": "Las contraseñas no coinciden."
            })
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Validate email exists."""
        if not User.objects.filter(email=value.lower()).exists():
            # Don't reveal if email exists for security
            # But we'll still return success
            pass
        return value.lower()


class TokenRefreshSerializer(serializers.Serializer):
    """
    Serializer for token refresh.
    """
    refreshToken = serializers.CharField(required=True)

