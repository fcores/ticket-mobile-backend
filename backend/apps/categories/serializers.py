"""
Serializers for categories app.
"""
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    ticketCount = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'createdAt', 'ticketCount']
        read_only_fields = ['id', 'createdAt']

    def get_ticketCount(self, obj):
        """Get count of tickets in this category."""
        # Note: This requires a related_name on the Ticket model
        # If not present, this will return 0
        if hasattr(obj, 'tickets'):
            return obj.tickets.count()
        return 0


class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating categories.
    """
    name = serializers.CharField(
        required=True,
        max_length=100,
        min_length=2
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True
    )

    class Meta:
        model = Category
        fields = ['name', 'description']

    def validate_name(self, value):
        """Validate category name is unique."""
        if Category.objects.filter(name__iexact=value.strip()).exists():
            raise serializers.ValidationError(
                "Ya existe una categoría con este nombre."
            )
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "El nombre debe tener al menos 2 caracteres."
            )
        return value.strip()


class CategoryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating categories.
    """
    name = serializers.CharField(
        required=False,
        max_length=100,
        min_length=2
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True
    )

    class Meta:
        model = Category
        fields = ['name', 'description']

    def validate_name(self, value):
        """Validate category name is unique (excluding current instance)."""
        if value:
            # Check if another category has this name
            existing = Category.objects.filter(name__iexact=value.strip()).exclude(
                id=self.instance.id
            )
            if existing.exists():
                raise serializers.ValidationError(
                    "Ya existe una categoría con este nombre."
                )
            if len(value.strip()) < 2:
                raise serializers.ValidationError(
                    "El nombre debe tener al menos 2 caracteres."
                )
        return value.strip() if value else value

