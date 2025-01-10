from typing import Dict, Optional
from datetime import datetime
import uuid
from rest_framework.response import Response
from .types import DataType

def response(
    data: DataType,
    status=None,
    template_name: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    exception: bool = False,
    content_type: Optional[str] = None
) -> Response:
    """
    Creates a standardized API response.

    Args:
        data: Response data containing status, message and optional data/errors
        status: HTTP status code
        template_name: Optional template name for rendering
        headers: Optional response headers
        exception: Whether this is an exception response
        content_type: Optional content type header

    Returns:
        Response object with standardized payload format including meta info
    """
    # Build response payload with standard format
    payload: DataType = {
        "status": data["status"],
        "message": data["message"],
        "data": data.get("data", None),
        "errors": data.get("errors", None),
        "meta": {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "response_time": "N/A",
            "documentation_url": "https://api.example.com/docs",
        }
    }

    return Response(
        data=payload,
        status=status,
        template_name=template_name,
        headers=headers,
        exception=exception,
        content_type=content_type
    )
