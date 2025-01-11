from typing import Literal
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from quick_utils.as_api_response_format import as_api_response_format


class IsVerified(BasePermission):
    def has_permission(self, request, view) -> Literal[True]:
        if request.user.is_superuser:
            return True

        # Check if the user is
        if not request.user.is_verified:
            raise PermissionDenied(as_api_response_format({
                "status": "failed",
                "message": "Please verify your account to continue.",
                "data": None,
                "errors": [{
                    "field": "account",
                    "code": "unverified_account",
                    "message": "You must verify your account to access this resource.",
                    "details": {
                        "verification_status": False
                    }
                }]
            }))

        return True
