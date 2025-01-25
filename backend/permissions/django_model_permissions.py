import logging
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


class DjangoModelPermissions(permissions.DjangoModelPermissions):
    """
    Custom authentication permission class that extends DRF's DjangoModelPermissions.
    Raises detailed PermissionDenied exception for unauthenticated or unauthorized requests.
    """

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view) -> bool:
        """Validates user permissions for view access."""
        if not getattr(view, 'queryset', None):
            raise PermissionDenied({
                "message": "Invalid View Configuration",
                "errors": [{
                    "field": "queryset",
                    "code": "missing_query_set",
                    "message": "Cannot apply DjangoModelPermissions to a view without a `queryset` attribute."
                }]
            })

        if request.user.is_superuser:
            # Grant full access to superusers
            logger.info(f"Superuser {request.user.username or request.user.email} authenticated successfully.")
            return True

        if not request.user or not request.user.is_staff:
            # Reject non-staff users with error details
            logger.warning(f"Unauthorized access attempt from {request.META.get('REMOTE_ADDR')}")
            raise PermissionDenied({
                "message": "Access Denied",
                "errors": [{
                    "field": "authentication",
                    "code": "unauthorized",
                    "message": "You do not have permission to access this resource.",
                    "details": {
                        "authentication_required": True
                    }
                }]
            })

        # Enforce DjangoModelPermissions for other users
        return super().has_permission(request, view)
