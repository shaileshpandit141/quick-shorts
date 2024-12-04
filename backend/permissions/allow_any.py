from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class AllowAny(BasePermission):
    def has_permission(self, request, view):
        # Allow access by default but raise custom error for specific conditions if needed
        return True  # Always allow access, just like AllowAny

    def deny(self, request, message=None):
        # Custom deny method for AllowAny-like behavior
        raise PermissionDenied({
            "status": "error",
            "message": message or "Permission denied.",
            "errors": {
                'non_field_errors': [
                    (message or "This action is not allowed.")
                ]
            }
        })
