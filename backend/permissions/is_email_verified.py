from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsEmailVerified(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user.is_superuser:
            return True

        # Check if the user is
        if not request.user.is_email_verified:
            raise PermissionDenied({
                "status": "failed",
                "message": "Please verify your email to continue.",
                "errors": {
                    'detail': [
                        "You must verify your email address to access this resource."
                    ]
                }
            })

        return True
