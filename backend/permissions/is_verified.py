from typing import Literal
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsVerified(BasePermission):
    def has_permission(self, request, view) -> Literal[True]:
        if request.user.is_superuser:
            return True

        # Check if the user is
        if not request.user.is_verified:
            raise PermissionDenied([{
                "field": "account",
                "code": "unverified_account",
                "message": "You must verify your account to access this resource.",
                "details": {
                    "verification_status": False
                }
            }])

        return True
