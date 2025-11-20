"""
Serializers for tickets app.
"""
from rest_framework import serializers
from .models import Ticket
from apps.users.serializers import UserSerializer


class TicketListSerializer(serializers.ModelSerializer):
    """
    Serializer for ticket list view.
    """
    displayStatus = serializers.CharField(source='display_status', read_only=True)
    displayPriority = serializers.CharField(source='display_priority', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    resolvedAt = serializers.DateTimeField(source='resolved_at', read_only=True)
    imageUrl = serializers.SerializerMethodField()
    
    creator = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    
    commentsCount = serializers.SerializerMethodField()
    attachmentsCount = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'status',
            'displayStatus',
            'priority',
            'displayPriority',
            'creator',
            'assignee',
            'createdAt',
            'updatedAt',
            'resolvedAt',
            'commentsCount',
            'attachmentsCount',
            'imageUrl'
        ]
    
    def get_imageUrl(self, obj):
        """Get full URL for ticket image."""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            # Fallback: construir URL con configuración por defecto
            from django.conf import settings
            base_url = getattr(settings, 'BASE_URL', 'http://10.0.2.2:8000')
            return f"{base_url}{obj.image.url}"
        return None

    def get_commentsCount(self, obj):
        """Get count of comments for this ticket."""
        return obj.comments.count()

    def get_attachmentsCount(self, obj):
        """Get count of attachments for this ticket."""
        return obj.attachments.count()


class TicketDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed ticket view.
    """
    displayStatus = serializers.CharField(source='display_status', read_only=True)
    displayPriority = serializers.CharField(source='display_priority', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    resolvedAt = serializers.DateTimeField(source='resolved_at', read_only=True)
    imageUrl = serializers.SerializerMethodField()
    
    creator = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'status',
            'displayStatus',
            'priority',
            'displayPriority',
            'creator',
            'assignee',
            'createdAt',
            'updatedAt',
            'resolvedAt',
            'imageUrl'
        ]
    
    def get_imageUrl(self, obj):
        """Get full URL for ticket image."""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            # Fallback: construir URL con configuración por defecto
            from django.conf import settings
            base_url = getattr(settings, 'BASE_URL', 'http://10.0.2.2:8000')
            return f"{base_url}{obj.image.url}"
        return None


class TicketCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a ticket.
    """
    title = serializers.CharField(
        required=True,
        max_length=200,
        min_length=5
    )
    description = serializers.CharField(
        required=True,
        min_length=10
    )
    priority = serializers.ChoiceField(
        choices=Ticket.PRIORITY_CHOICES,
        default='medium'
    )
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'image']

    def validate_title(self, value):
        """Validate title."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "El título debe tener al menos 5 caracteres."
            )
        return value.strip()

    def validate_description(self, value):
        """Validate description."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "La descripción debe tener al menos 10 caracteres."
            )
        return value.strip()

    def create(self, validated_data):
        """Create ticket with creator."""
        request = self.context.get('request')
        validated_data['creator'] = request.user
        return super().create(validated_data)


class TicketUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a ticket.
    """
    title = serializers.CharField(
        required=False,
        max_length=200,
        min_length=5
    )
    description = serializers.CharField(required=False, min_length=10)
    status = serializers.ChoiceField(
        choices=Ticket.STATUS_CHOICES,
        required=False
    )
    priority = serializers.ChoiceField(
        choices=Ticket.PRIORITY_CHOICES,
        required=False
    )
    assigneeId = serializers.IntegerField(
        source='assignee_id',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'assigneeId']

    def validate_title(self, value):
        """Validate title."""
        if value and len(value.strip()) < 5:
            raise serializers.ValidationError(
                "El título debe tener al menos 5 caracteres."
            )
        return value.strip() if value else value

    def validate_description(self, value):
        """Validate description."""
        if value and len(value.strip()) < 10:
            raise serializers.ValidationError(
                "La descripción debe tener al menos 10 caracteres."
            )
        return value.strip() if value else value

    def validate_assigneeId(self, value):
        """Validate assignee exists and has proper role."""
        if value is not None:
            from apps.users.models import User
            try:
                user = User.objects.get(id=value)
                if user.role not in ['support', 'sysAdmin']:
                    raise serializers.ValidationError(
                        "El usuario asignado debe ser soporte o administrador."
                    )
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "El usuario asignado no existe."
                )
        return value

    def update(self, instance, validated_data):
        """Update ticket."""
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        
        if 'assignee_id' in validated_data:
            instance.assignee_id = validated_data['assignee_id']
        
        instance.save()
        return instance


class TicketStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating only ticket status.
    """
    status = serializers.ChoiceField(
        choices=Ticket.STATUS_CHOICES,
        required=True
    )

    class Meta:
        model = Ticket
        fields = ['status']

    def validate_status(self, value):
        """Validate status transition."""
        instance = self.instance
        
        # Business rules for status transitions
        if instance.status == 'closed' and value != 'closed':
            raise serializers.ValidationError(
                "No se puede reabrir un ticket cerrado."
            )
        
        if value == 'resolved' and not instance.assignee:
            raise serializers.ValidationError(
                "El ticket debe estar asignado antes de marcarse como resuelto."
            )
        
        return value


class TicketAssignSerializer(serializers.Serializer):
    """
    Serializer for assigning ticket to user.
    """
    assigneeId = serializers.IntegerField(required=True, allow_null=True)

    def validate_assigneeId(self, value):
        """Validate assignee."""
        if value is not None:
            from apps.users.models import User
            try:
                user = User.objects.get(id=value)
                if user.role not in ['support', 'sysAdmin']:
                    raise serializers.ValidationError(
                        "Solo se puede asignar a usuarios de soporte o administradores."
                    )
                if not user.is_active:
                    raise serializers.ValidationError(
                        "No se puede asignar a un usuario inactivo."
                    )
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "El usuario no existe."
                )
        return value

