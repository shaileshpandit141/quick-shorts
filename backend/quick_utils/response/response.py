from typing import Dict, Optional
from rest_framework.response import Response as DRFResponse
from ..types import ResponseDataType


class Response(DRFResponse):
    """A custom Response class to standardize API responses"""

    def __init__(
        self,
        data: ResponseDataType,
        status: Optional[int] = None,
        template_name: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None,
    ):
        super().__init__(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )
