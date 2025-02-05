import logging
from typing import Literal

from rest_framework import permissions

logger = logging.getLogger(__name__)


class AllowAny(permissions.AllowAny):
    """A permission class that allows unrestricted access.

    This class extends DRF's base AllowAny permission and always returns True,
    while adding debug logging of the requesting user.
    """

    def has_permission(self, request, view) -> Literal[True]:
        """Grant permission and log the request details."""
        user_info = request.user if request.user.is_authenticated else "Anonymous"
        logger.debug(
            f"Allowing request for user: {user_info}, "
            f"IP: {request.META.get('REMOTE_ADDR')}, "
            f"Endpoint: {request.path}"
        )
        return True
