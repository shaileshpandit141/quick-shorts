"""
Provides core API components for handling requests and responses.

This module imports and exposes the main classes needed to handle API requests,
define response data types, and build standardized API responses. It abstracts
away unnecessary implementation details and only exposes the essential public
interface.
"""

from rest_framework.response import Response
from .base_apiview import BaseAPIView
from .apiview import APIView

# Public interface exposing only necessary functionality for API development
__all__ = ["APIView", "BaseAPIView", "Response"]
