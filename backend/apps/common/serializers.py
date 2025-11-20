"""
Serializers for common app.
"""
from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    """
    Serializer for health check response.
    """
    status = serializers.CharField()
    message = serializers.CharField()
    timestamp = serializers.DateTimeField()
    version = serializers.CharField()
    database = serializers.CharField()
    services = serializers.DictField()


class ErrorResponseSerializer(serializers.Serializer):
    """
    Serializer for standardized error responses.
    """
    error = serializers.CharField()
    details = serializers.DictField(required=False)
    timestamp = serializers.DateTimeField()


class SuccessResponseSerializer(serializers.Serializer):
    """
    Serializer for standardized success responses.
    """
    message = serializers.CharField()
    data = serializers.DictField(required=False)
    timestamp = serializers.DateTimeField()

