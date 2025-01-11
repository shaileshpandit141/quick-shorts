from rest_framework.permissions import IsAuthenticated as DRFIsAuthenticated
from rest_framework.exceptions import PermissionDenied
from quick_utils.as_api_response_format import as_api_response_format

class IsAuthenticated(DRFIsAuthenticated):
    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            # Raising a custom permission denied exception with a custom message
            raise PermissionDenied(as_api_response_format({
                "status": "failed",
                "message": "Please sign in to continue.",
                "data": None,
                "errors": [{
                    "field": "authentication",
                    "code": "not_authenticated",
                    "message": "You must be authenticated to access this resource.",
                    "details": {
                        "required": True
                    }
                }]
            }))

        return True
