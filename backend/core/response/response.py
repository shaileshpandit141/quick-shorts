from typing import Optional

from rest_framework import response

from .response_types import TypeResponsePayload


class Response(response.Response):
    """A custom Response class to standardize API responses"""

    def __init__(
        self,
        data: TypeResponsePayload,
        status: Optional[int] = None,
        template_name: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None,
    ) -> None:
        super().__init__(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )
