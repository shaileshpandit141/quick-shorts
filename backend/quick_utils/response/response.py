from typing import Dict, Optional
from datetime import datetime
import uuid
from rest_framework.response import Response as DRFResponse
from ..types import ResponseDataType, MetaType


class Response(DRFResponse):
    """
    A custom Response class to standardize API responses with metadata.
    """

    def __init__(
        self,
        data: ResponseDataType,
        status: Optional[int] = None,
        template_name: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None,
    ):
        # Standardized response payload structure
        payload = {
            "status": data.get("status", "success"),
            "message": data.get("message", "Request processed successfully."),
            "data": data.get("data", None),
            "errors": data.get("errors", []),
            "meta": self._generate_meta(data.get("meta", None)),
        }

        # Initialize the base Response class with the standardized payload
        super().__init__(
            data=payload,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )

    @staticmethod
    def _generate_meta(custom_meta: MetaType | None) -> MetaType:
        """
        Generate the meta field with default values and merge custom meta if provided.
        """
        default_meta: MetaType = {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "documentation_url": "https://api.example.com/docs",
            "rate_limit": []
        }
        if custom_meta is not None:
            default_meta.update(custom_meta)
        return default_meta
