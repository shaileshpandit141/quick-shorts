"""
This module provides a URLBuilder class that constructs a full URL from a Django HttpRequest.
It supports optional viewname-based URL reversing, custom path segments, query parameters,
and additional arguments (args/kwargs) for the reverse function. A 'safe' parameter is
also included for fine-tuned query string encoding.

Example Usage:
    ## 1. Construct a URL using a Django viewname and keyword arguments
    builder = URLBuilder(
        request=request,
        viewname="post_detail",
        kwargs={"slug": "my-post"},
        query_dict={"page": 2, "size": 25}
    )
    print(builder.build())  # Output: https://example.com/posts/my-post?page=2&size=25

    ## 2. Construct a URL with a custom path instead of using reverse
    builder = URLBuilder(
        request=request,
        path="api/v1/items",
        query_dict={"sort": "desc"}
    )
    print(builder.build())  # Output: https://example.com/api/v1/items?sort=desc

    ## 3. Construct a URL using reverse with positional args
    builder = URLBuilder(
        request=request,
        viewname="category_list",
        args=["electronics"]
    )
    print(builder.build())  # Output: https://example.com/categories/electronics
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Optional

from django.http import HttpRequest, QueryDict
from django.urls import NoReverseMatch, reverse

# Configure module-level logger
logger = logging.getLogger(__name__)


@dataclass
class URLBuilder:
    """
    Constructs a fully qualified URL using a Django HttpRequest, with optional support for:
    - URL reversing via `viewname`
    - Additional path segments
    - Query parameters
    - URL-encoded query string customization

    Attributes:
        request (HttpRequest): The current Django request used to determine the protocol and host.
        viewname (Optional[str]): The Django URL pattern name to reverse. If provided, `args` and `kwargs`
                                  will be used to resolve the URL.
        path (str): Additional path segments to append after the reversed URL or base host.
        query_dict (dict[str, Any]): A dictionary of query parameters to append to the URL.
        safe (Optional[str]): Characters that should not be URL encoded in the query string.
        args (list[Any]): Positional arguments for reverse URL resolution (e.g., ID in `/posts/<id>/`).
        kwargs (dict[str, Any]): Keyword arguments for reverse URL resolution (e.g., `slug="my-post"`).
        current_app (Optional[str]): The current application namespace for Django's `reverse` function.

    Example Usage:
        ## Reverse a URL pattern and add query parameters
        builder = URLBuilder(
            request=request,
            viewname="post_detail",
            kwargs={"slug": "my-post"},
            query_dict={"page": 2, "size": 25}
        )
        print(builder.build())  # Output: https://example.com/posts/my-post?page=2&size=25

        ## Construct a URL with a custom path and query parameters
        builder = URLBuilder(
            request=request,
            path="api/v1/items",
            query_dict={"sort": "desc"}
        )
        print(builder.build())  # Output: https://example.com/api/v1/items?sort=desc

        ## Construct a URL using reverse with positional args
        builder = URLBuilder(
            request=request,
            viewname="category_list",
            args=["electronics"]
        )
        print(builder.build())  # Output: https://example.com/categories/electronics
    """

    request: HttpRequest
    viewname: Optional[str] = None
    path: str = ""
    query_dict: dict[str, Any] = field(default_factory=dict)
    safe: Optional[str] = None
    args: list[Any] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)
    current_app: Optional[str] = None

    def build(self) -> str:
        """
        Constructs and returns a fully-qualified URL.

        The constructed URL includes:
            - The protocol (http or https), determined from the HttpRequest.
            - The request host.
            - A reversed URL if a `viewname` is provided.
            - An additional custom path if specified.
            - A URL-encoded query string if `query_dict` contains parameters.

        Returns:
            str: The fully constructed URL.
        """
        protocol = "https" if self.request.is_secure() else "http"
        host = self.request.get_host()
        logger.debug(f"Using protocol: {protocol} and host: {host}")

        base_url = f"{protocol}://{host}"

        if self.viewname:
            try:
                reversed_url = reverse(
                    viewname=self.viewname,
                    args=self.args,
                    kwargs=self.kwargs,
                    current_app=self.current_app,
                )
                base_url += reversed_url
                logger.debug(
                    f"Resolved viewname '{self.viewname}' to URL: {reversed_url}"
                )
            except NoReverseMatch:
                logger.warning(
                    f"NoReverseMatch: Could not resolve viewname '{self.viewname}'"
                )

        if self.path:
            logger.debug(f"Appending path: {self.path}")
            base_url += f"/{self.path.lstrip('/')}"

        if self.query_dict:
            logger.debug(f"Adding query parameters: {self.query_dict}")
            query = QueryDict("", mutable=True)
            query.update(self.query_dict)
            query_string = query.urlencode(safe=self.safe)
            base_url += f"?{query_string}"
            logger.debug(f"Constructed query string: {query_string}")

        logger.info("Constructed URL: %s", base_url)
        return base_url
