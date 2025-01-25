from typing import Literal
import logging
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


class IsVerified(BasePermission):
    """
    Permission class that checks if a user is verified.

    Only allows access to verified users or superusers.
    Raises PermissionDenied with details if the user is unverified or unauthenticated.
    """

    def has_permission(self, request, view) -> Literal[True]:
        """
        Check if the user is verified or a superuser.
        """
        # Handle unauthenticated users
        if not request.user or not request.user.is_authenticated:
            logger.warning(
                f"Unauthenticated access attempt to {request.method} {request.path} "
                f"from {request.META.get('REMOTE_ADDR')}."
            )
            raise PermissionDenied({
                "message": "Authentication Required",
                "errors": [{
                    "field": "authentication",
                    "code": "not_authenticated",
                    "message": "You must be logged in to access this resource.",
                    "details": {
                        "authenticated": False
                    }
                }]
            })

        # Allow superusers unconditional access
        if request.user.is_superuser:
            logger.info(
                f"Superuser {request.user.username or request.user.email} authenticated successfully "
                f"for {request.method} {request.path}."
            )
            return True

        # Check if the user's account is verified
        if not getattr(request.user, 'is_verified', False):
            logger.warning(
                f"Unverified user {request.user.id} ({request.user.email}) attempted to access "
                f"{request.method} {request.path}."
            )
            raise PermissionDenied({
                "message": "Account Not Verified",
                "errors": [{
                    "field": "account",
                    "code": "unverified_account",
                    "message": "Your account must be verified to access this resource.",
                    "details": {
                        "verification_status": False,
                        "user_id": request.user.id,
                        "user_email": request.user.email
                    }
                }]
            })

        # Log successful verification
        logger.info(
            f"Verified user {request.user.username or request.user.email} successfully accessed "
            f"{request.method} {request.path}."
        )
        return True
