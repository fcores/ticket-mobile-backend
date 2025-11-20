"""
Serializers for attachments app.
"""
from rest_framework import serializers
from .models import Attachment
from apps.users.serializers import UserSerializer


class AttachmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Attachment model.
    """
    uploadedBy = UserSerializer(source='uploaded_by', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    isPrivate = serializers.BooleanField(source='is_private', read_only=True)
    ticketId = serializers.IntegerField(source='ticket_id', read_only=True)
    originalFilename = serializers.CharField(source='original_filename', read_only=True)
    fileSize = serializers.IntegerField(source='file_size', read_only=True)
    mimeType = serializers.CharField(source='mime_type', read_only=True)
    fileUrl = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            'id',
            'originalFilename',
            'fileUrl',
            'fileSize',
            'mimeType',
            'uploadedBy',
            'ticketId',
            'createdAt',
            'isPrivate'
        ]

    def get_fileUrl(self, obj):
        """Get file URL."""
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            if request:
                return request.build_absolute_uri(obj.file.url)
            # Fallback: construir URL con configuración por defecto
            from django.conf import settings
            base_url = getattr(settings, 'BASE_URL', 'http://10.0.2.2:8000')
            return f"{base_url}{obj.file.url}"
        return None


class AttachmentUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading attachments.
    """
    file = serializers.FileField(required=True)
    isPrivate = serializers.BooleanField(
        source='is_private',
        default=False,
        required=False
    )

    class Meta:
        model = Attachment
        fields = ['file', 'isPrivate']

    def validate_file(self, value):
        """Validate file upload."""
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError(
                f"El archivo no puede exceder 10MB. Tamaño actual: {value.size / 1024 / 1024:.2f}MB"
            )
        
        # Check file extension
        allowed_extensions = [
            '.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp',
            '.zip', '.rar', '.7z'
        ]
        
        import os
        file_extension = os.path.splitext(value.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(
                f"Tipo de archivo no permitido. Extensiones permitidas: {', '.join(allowed_extensions)}"
            )
        
        return value

    def validate_isPrivate(self, value):
        """Validate private attachment permission."""
        request = self.context.get('request')
        if value and request:
            user = request.user
            if user.role not in ['support', 'sysAdmin']:
                raise serializers.ValidationError(
                    "Solo el personal de soporte puede subir archivos privados."
                )
        return value

    def create(self, validated_data):
        """Create attachment with uploader and ticket."""
        request = self.context.get('request')
        ticket = self.context.get('ticket')
        
        validated_data['uploaded_by'] = request.user
        validated_data['ticket'] = ticket
        
        return super().create(validated_data)

