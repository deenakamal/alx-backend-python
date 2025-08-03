from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own data.
    """

    def has_object_permission(self, request, view, obj):
        # Check if object has a 'user' field or 'owner'
        return obj.user == request.user
