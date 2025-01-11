from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from quick_utils.as_api_response_format import as_api_response_format

class AllowAny(BasePermission):
    def has_permission(self, request, view):
        # Allow access by default but raise custom error for specific conditions if needed
        return True  # Always allow access, just like AllowAny

    def deny(self, request, message=None):
        # Custom deny method for AllowAny-like behavior
        raise PermissionDenied(as_api_response_format({
            "status": "failed",
            "message": message or "Permission denied.",
            "data": None,
            "errors": [{
                "field": "request",
                "code": "permission_denied",
                "message": message or "This action is not allowed.",
                "details": None
            }]
        }))
