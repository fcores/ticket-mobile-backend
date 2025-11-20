"""
Custom permissions for users app.
"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission to check if user is a system administrator.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'sysAdmin'
        )


class IsSupportOrAdmin(permissions.BasePermission):
    """
    Permission to check if user is support or admin.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['support', 'sysAdmin']
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to check if user is the owner of the object or an admin.
    """
    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.role == 'sysAdmin':
            return True
        
        # Check if object has a user/creator/author attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'creator'):
            return obj.creator == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user
        
        return False

