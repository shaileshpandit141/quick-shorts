from typing import Dict, Optional
from datetime import datetime
import uuid
from rest_framework.response import Response
from .response_types import ResponseDataType

def response(
    data: ResponseDataType,
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
    payload: ResponseDataType = {
        "status": data["status"],
        "message": data["message"],
        "data": data.get("data", None),
        "errors": data.get("errors", None),
        "meta": None
    }

    meta = data.get("meta", None)
    if meta is None:
        payload["meta"] = {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "documentation_url": "https://api.example.com/docs"
        }
    else:
        payload["meta"] = {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "documentation_url": "https://api.example.com/docs",
            **meta
        }

    return Response(
        data=payload,
        status=status,
        template_name=template_name,
        headers=headers,
        exception=exception,
        content_type=content_type
    )
