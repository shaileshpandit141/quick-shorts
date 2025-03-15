"""
This module provides a URLBuilder class that constructs a full URL from a Django HttpRequest,
an optional path, and query parameters. It also logs key steps during URL construction.
"""

import logging
from typing import Any
from dataclasses import dataclass
from django.http import QueryDict, HttpRequest

# Configure module-level logger
logger = logging.getLogger(__name__)


@dataclass
class URLBuilder:
    """
    URLBuilder constructs the full URL based on the provided HttpRequest, an optional
    path, and query parameters.

    Example:
        ### Initialize URLBuilder with an optional path and query parameters
        builder = URLBuilder(
            request=request,
            path="/api/v1/items",
            query_dict={"page": 2, "size": 25}
        )
        ### Build the full URL
        full_url = builder.build()
        print(full_url)  # Output: https://example.com/api/v1/items?page=2&size=25
    """

    request: HttpRequest
    path: str = ""
    query_dict: dict[str, Any] | None = None
    safe: str | None = None

    def build(self) -> str:
        """
        Constructs the full URL.

        Returns:
            str: The fully constructed URL, consisting of:
                - The protocol (http or https) determined from the request
                - The host from the request
                - An optional path appended to the host
                - Optional query parameters appended as a query string
        """
        protocol = "https" if self.request.is_secure() else "http"
        host = self.request.get_host()
        logger.debug("Using protocol: %s and host: %s", protocol, host)
        base_url = f"{protocol}://{host}/"

        if self.path:
            logger.debug("Appending path: %s", self.path)
            base_url += self.path.lstrip("/")

        if self.query_dict:
            logger.debug("Adding query parameters: %s", self.query_dict)
            query = QueryDict(mutable=True)
            query.update(self.query_dict)
            query_string = query.urlencode(safe=self.safe)
            base_url += f"?{query_string}"
            logger.debug("Constructed query string: %s", query_string)

        logger.info("Constructed URL: %s", base_url)
        return base_url
