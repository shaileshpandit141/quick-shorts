from typing import Literal
import logging
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


logger = logging.getLogger(__name__)


class IsVerified(BasePermission):
    """
    Permission class that checks if a user is verified.

    Only allows access to verified users or superusers.
    Raises PermissionDenied with details if user is unverified.
    """
    def has_permission(self, request, view) -> Literal[True]:
        # Allow superusers unconditional access
        if request.user.is_superuser:
            return True

        # Check if user account is verified
        if not request.user.is_verified:
            logger.warning(
                f"Unverified user {request.user.id} attempted to access protected resource"
            )
            raise PermissionDenied([{
                "field": "account",
                "code": "unverified_account",
                "message": "You must verify your account to access this resource.",
                "details": {
                    "verification_status": False
                }
            }])

        return True
