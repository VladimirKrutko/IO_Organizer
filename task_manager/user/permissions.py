from rest_framework.permissions import BasePermission


class UserUpdatePermission(BasePermission):
    """
    Class with manager permission
    """

    def has_permission(self, request, view):
        if request.user.role == 'moderator':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author != request.user:
            return True
        return False
