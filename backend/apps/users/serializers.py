"""
Serializers for users app.
"""
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    firstName = serializers.CharField(source='first_name', read_only=True)
    lastName = serializers.CharField(source='last_name', read_only=True)
    fullName = serializers.CharField(source='full_name', read_only=True)
    displayRole = serializers.CharField(source='display_role', read_only=True)
    profilePicture = serializers.ImageField(source='profile_picture', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    lastLogin = serializers.DateTimeField(source='last_login', read_only=True)
    isActive = serializers.BooleanField(source='is_active', read_only=True)
    isStaff = serializers.BooleanField(source='is_staff', read_only=True)
    isSuperuser = serializers.BooleanField(source='is_superuser', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'firstName',
            'lastName',
            'fullName',
            'role',
            'displayRole',
            'profilePicture',
            'createdAt',
            'lastLogin',
            'isActive',
            'isStaff',
            'isSuperuser'
        ]
        read_only_fields = ['id', 'username', 'email', 'createdAt']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    firstName = serializers.CharField(
        source='first_name',
        min_length=2,
        max_length=50,
        required=False
    )
    lastName = serializers.CharField(
        source='last_name',
        min_length=2,
        max_length=50,
        required=False
    )
    profilePicture = serializers.ImageField(
        source='profile_picture',
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'profilePicture']

    def validate_firstName(self, value):
        """Validate first name."""
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError(
                "El nombre debe tener al menos 2 caracteres."
            )
        return value.strip()

    def validate_lastName(self, value):
        """Validate last name."""
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError(
                "El apellido debe tener al menos 2 caracteres."
            )
        return value.strip()

    def update(self, instance, validated_data):
        """Update user profile."""
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data['profile_picture']
        
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for user lists (admin).
    """
    firstName = serializers.CharField(source='first_name', read_only=True)
    lastName = serializers.CharField(source='last_name', read_only=True)
    fullName = serializers.CharField(source='full_name', read_only=True)
    displayRole = serializers.CharField(source='display_role', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    lastLogin = serializers.DateTimeField(source='last_login', read_only=True)
    isActive = serializers.BooleanField(source='is_active', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'firstName',
            'lastName',
            'fullName',
            'role',
            'displayRole',
            'createdAt',
            'lastLogin',
            'isActive'
        ]


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user role (admin only).
    """
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True
    )

    class Meta:
        model = User
        fields = ['role']

    def validate_role(self, value):
        """Validate role."""
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError(
                f"Rol inválido. Debe ser uno de: {', '.join(valid_roles)}"
            )
        return value


class UserActivationSerializer(serializers.ModelSerializer):
    """
    Serializer for activating/deactivating users (admin only).
    """
    isActive = serializers.BooleanField(source='is_active', required=True)

    class Meta:
        model = User
        fields = ['isActive']

