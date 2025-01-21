from typing import Literal
from rest_framework import permissions
import logging


logger = logging.getLogger(__name__)


class AllowAny(permissions.AllowAny):
    """A permission class that allows unrestricted access.

    This class extends DRF's base AllowAny permission and always returns True,
    while adding debug logging of the requesting user.
    """

    def has_permission(self, request, view) -> Literal[True]:
        # Log user access for debugging purposes
        logger.debug(f"Allowing request for {request.user}")
        return True
