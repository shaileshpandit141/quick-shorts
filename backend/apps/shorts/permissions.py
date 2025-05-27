from typing import Any, Literal

from rest_framework.permissions import BasePermission
from shorts.models.short_video import ShortVideo


class CanUpdateAndDelete(BasePermission):
    def has_object_permission(
        self, request, view, obj: ShortVideo
    ) -> Any | Literal[True]:
        if request.method in ("PUT", "PATCH", "DELETE"):
            return obj.owner == request.user
        return True
