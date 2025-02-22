import json
import time
import uuid
from logging import getLogger
from typing import Any

from django.http import JsonResponse
from rest_framework.response import Response

from ..utils import (
    add_response_headers,
    add_throttle_details_in_header,
    get_meta,
    handle_response,
)

# Configure logger
logger = getLogger(__name__)


# Main Middleware Class
class ResponseMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.logger = logger

    # Main Entry Point
    def __call__(self, request) -> JsonResponse | Any:
        start_time = time.perf_counter()
        request_id = str(uuid.uuid4())
        self.logger.info(
            f"Processing request {request_id} - {request.method} {request.path}"
        )

        try:
            response = self.get_response(request)
            response_time = f"{round(time.perf_counter() - start_time, 5)} seconds"
            throttles = getattr(response, "throttles", [])

            if isinstance(response, JsonResponse):
                data = json.loads(response.content.decode("utf-8"))
                return handle_response(
                    data, response, throttles, response_time, request, request_id
                )

            if isinstance(response, Response):
                return handle_response(
                    response.data,
                    response,
                    throttles,
                    response_time,
                    request,
                    request_id,
                )

            if response.status_code == 429:
                self.logger.warning(f"Rate limit exceeded for request {request_id}")
                json_response = JsonResponse(
                    {
                        "status": "failed",
                        "status_code": 429,
                        "message": "Too many requests. Please wait before trying again.",
                        "data": None,
                        "errors": [
                            {
                                "field": "throttle",
                                "code": "throttle_limit_exceeded",
                                "message": response.headers.get("Retry-After", "N/A"),
                                "details": None,
                            }
                        ],
                        "meta": get_meta(
                            {"rate_limit": throttles}, response_time, request_id
                        ),
                    },
                    status=response.status_code,
                )
                add_response_headers(
                    json_response,
                    {
                        "X-Processing-Time": response_time,
                        "X-Request-ID": request_id,
                        "X-Status-Code": "429",
                    },
                )
                add_throttle_details_in_header(json_response, throttles)
                return json_response

            # Log non-API requests before returning response
            add_response_headers(
                response,
                {
                    "X-Request-ID": request_id,
                    "X-Status-Code": str(response.status_code),
                },
            )
            add_throttle_details_in_header(response, throttles)
            return response

        except Exception as error:
            self.logger.exception(
                f"An unhandled exception occurred while processing request {request_id}: {str(error)}"
            )
            json_response = JsonResponse(
                {
                    "status": "failed",
                    "status_code": 500,
                    "message": "Internal server error",
                    "data": None,
                    "errors": [
                        {
                            "field": "server",
                            "code": "internal_error",
                            "message": str(error),
                            "details": None,
                        }
                    ],
                    "meta": get_meta({}, "N/A", request_id),
                },
                status=500,
            )
            add_response_headers(
                json_response,
                {
                    "X-Processing-Time": "N/A",
                    "X-Request-ID": request_id,
                    "X-Status-Code": "500",
                },
            )
            return json_response
