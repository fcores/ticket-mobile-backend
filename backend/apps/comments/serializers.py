"""
Serializers for comments app.
"""
from rest_framework import serializers
from .models import Comment
from apps.users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """
    author = UserSerializer(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    isPrivate = serializers.BooleanField(source='is_private', read_only=True)
    ticketId = serializers.IntegerField(source='ticket_id', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'author',
            'ticketId',
            'createdAt',
            'isPrivate'
        ]
        read_only_fields = ['id', 'author', 'createdAt', 'ticketId']


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating comments.
    """
    text = serializers.CharField(
        required=True,
        min_length=1,
        max_length=2000
    )
    isPrivate = serializers.BooleanField(
        source='is_private',
        default=False,
        required=False
    )

    class Meta:
        model = Comment
        fields = ['text', 'isPrivate']

    def validate_text(self, value):
        """Validate comment text."""
        if not value or len(value.strip()) < 1:
            raise serializers.ValidationError(
                "El comentario no puede estar vacío."
            )
        if len(value) > 2000:
            raise serializers.ValidationError(
                "El comentario no puede exceder 2000 caracteres."
            )
        return value.strip()

    def validate_isPrivate(self, value):
        """Validate private comment permission."""
        request = self.context.get('request')
        if value and request:
            user = request.user
            if user.role not in ['support', 'sysAdmin']:
                raise serializers.ValidationError(
                    "Solo el personal de soporte puede crear comentarios privados."
                )
        return value

    def create(self, validated_data):
        """Create comment with author and ticket."""
        request = self.context.get('request')
        ticket = self.context.get('ticket')
        
        validated_data['author'] = request.user
        validated_data['ticket'] = ticket
        
        return super().create(validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating comments.
    """
    text = serializers.CharField(
        required=True,
        min_length=1,
        max_length=2000
    )

    class Meta:
        model = Comment
        fields = ['text']

    def validate_text(self, value):
        """Validate comment text."""
        if not value or len(value.strip()) < 1:
            raise serializers.ValidationError(
                "El comentario no puede estar vacío."
            )
        if len(value) > 2000:
            raise serializers.ValidationError(
                "El comentario no puede exceder 2000 caracteres."
            )
        return value.strip()

