"""
Serializers for metrics app.
"""
from rest_framework import serializers


class TicketMetricsSerializer(serializers.Serializer):
    """
    Serializer for ticket metrics overview.
    """
    total = serializers.IntegerField()
    open = serializers.IntegerField()
    inProgress = serializers.IntegerField()
    resolved = serializers.IntegerField()
    closed = serializers.IntegerField()
    canceled = serializers.IntegerField()
    unassigned = serializers.IntegerField()


class TicketPriorityMetricsSerializer(serializers.Serializer):
    """
    Serializer for ticket priority metrics.
    """
    low = serializers.IntegerField()
    medium = serializers.IntegerField()
    high = serializers.IntegerField()
    urgent = serializers.IntegerField()


class TicketPerformanceSerializer(serializers.Serializer):
    """
    Serializer for ticket performance metrics.
    """
    averageResolutionTime = serializers.FloatField()  # in hours
    totalResolved = serializers.IntegerField()
    totalCreatedToday = serializers.IntegerField()
    totalCreatedThisWeek = serializers.IntegerField()
    totalCreatedThisMonth = serializers.IntegerField()
    resolutionRate = serializers.FloatField()  # percentage


class UserActivitySerializer(serializers.Serializer):
    """
    Serializer for user activity metrics.
    """
    userId = serializers.IntegerField()
    userName = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    ticketsCreated = serializers.IntegerField()
    ticketsAssigned = serializers.IntegerField()
    ticketsResolved = serializers.IntegerField()
    commentsPosted = serializers.IntegerField()
    lastActivity = serializers.DateTimeField()


class SystemHealthSerializer(serializers.Serializer):
    """
    Serializer for system health metrics.
    """
    status = serializers.CharField()
    totalUsers = serializers.IntegerField()
    activeUsers = serializers.IntegerField()
    totalTickets = serializers.IntegerField()
    openTickets = serializers.IntegerField()
    urgentTickets = serializers.IntegerField()
    unassignedTickets = serializers.IntegerField()
    averageResponseTime = serializers.FloatField()  # in hours

