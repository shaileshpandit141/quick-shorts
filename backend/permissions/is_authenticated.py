import logging
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


logger = logging.getLogger(__name__)


class IsAuthenticated(permissions.IsAuthenticated):
    """
    Custom authentication permission class that extends DRF's IsAuthenticated.
    Raises detailed PermissionDenied exception for unauthenticated requests.
    """
    def has_permission(self, request, view) -> bool:
        """Check if the request has valid authentication."""

        if request.user.is_superuser:
            # Allow superusers to bypass further authentication checks
            logger.info(f"Superuser {request.user.username or request.user.email} authenticated successfully.")
            return True

        if not request.user or not request.user.is_authenticated:
            # Log and raise custom permission denied exception
            logger.warning(f"Unauthenticated access attempt from {request.META.get('REMOTE_ADDR')}")
            raise PermissionDenied({
                "message": "Authentication Required",
                "errors": [{
                    "field": "authentication",
                    "code": "not_authenticated",
                    "message": "You must include a valid authentication token in the Authorization header.",
                    "details": {
                        "required": True,
                        "header": "Authorization: Token <your-token-here>"
                    }
                }]
            })

        return True
