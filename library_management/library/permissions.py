from rest_framework.permissions import BasePermission

class IsMember(BasePermission):
    """
    Custom permission to grant access only to users with the 'member' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'member'
