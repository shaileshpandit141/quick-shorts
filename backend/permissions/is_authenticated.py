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

        if not request.user or not request.user.is_authenticated:
            # Log and raise custom permission denied exception
            logger.warning(f"Unauthenticated access attempt from {request.META.get('REMOTE_ADDR')}")
            raise PermissionDenied([{
                "field": "authentication",
                "code": "not_authenticated",
                "message": "You must be authenticated to access this resource.",
                "details": {
                    "required": True
                }
            }])

        return True
