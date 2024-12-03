from rest_framework.permissions import BasePermission

class IsEmailVerified(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'is_email_verified')
            and request.user.is_email_verified
        )
