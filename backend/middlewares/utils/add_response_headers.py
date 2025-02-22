from logging import getLogger
from typing import Any, Dict

from django.http import JsonResponse
from rest_framework.response import Response

# Configure logger
logger = getLogger(__name__)


# Header Management
def add_response_headers(response: Any, headers: Dict[str, str]) -> None:
    try:
        if isinstance(response, (JsonResponse, Response)):
            for key, value in headers.items():
                response[key] = value
        elif hasattr(response, "headers"):
            for key, value in headers.items():
                response.headers[key] = value
        logger.debug(f"Added headers: {headers}")
    except Exception as e:
        logger.error(f"Error adding headers: {str(e)}")
