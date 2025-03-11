"""
This module imports and exposes BaseModelViewSet and BaseReadOnlyModelViewSet classes.

BaseModelViewSet provides a complete set of default CRUD actions.
BaseReadOnlyModelViewSet provides default 'read-only' actions.
"""

from .base_model_viewset import BaseModelViewSet
from .base_read_only_model_viewset import BaseReadOnlyModelViewSet

__all__ = ["BaseModelViewSet", "BaseReadOnlyModelViewSet"]
