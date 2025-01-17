from typing import Any, Dict, List, TypedDict, NotRequired, Optional
import time
from datetime import datetime  # type: ignore
import uuid
from django.http import JsonResponse
from rest_framework.response import Response
import json


class InvalidDataFormatError(Exception):
    def __init__(
        self,
        message: str = "Internal server error occurred",
        code: str = "server_error",
        field: str = "server",
        details: Any = "Server encountered an error processing the request"
    ) -> None:
        self.error_dict = {
            "field": field,
            "code": code,
            "message": message,
            "details": {
                "help": details
            }
        }
        super().__init__(str(self.error_dict))


class DataType(TypedDict):
    message: str
    data: NotRequired[Dict[str, Any]]
    errors: NotRequired[List[Dict[str, Any]]]


class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_meta(
        self,
        custom_meta: Optional[Dict[str, Any]] = None,
        response_time: str = "N/A"
    ) -> Dict[str, Any]:
        """Generate the meta field with default values and merge custom meta if provided."""
        default_meta = {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "response_time": response_time,
            "documentation_url": "N/A",
        }
        if custom_meta is not None:
            default_meta.update(custom_meta)
        return default_meta

    def is_data_valid(
        self,
        data: DataType | None,
        expected_keys: List[str]
    ) -> DataType:
        """Check if the response data format matches expected keys"""
        if not data or not isinstance(data, dict):
            raise InvalidDataFormatError(
                message="Response data must be a valid dictionary format.",
                code="invalid_format",
                details="The response data is either missing or not in dictionary format"
            )

        data_keys = sorted(data.keys())
        expected_keys.sort()

        if data_keys != expected_keys:
            raise InvalidDataFormatError(
                message="Response data is missing required fields or contains invalid fields.",
                code="invalid_keys",
                details=f"Expected fields: {', '.join(expected_keys)}. Received fields: {', '.join(data_keys)}"
            )

        return data

    def __call__(self, request):
        start_time = time.perf_counter()
        response = self.get_response(request)
        response_time = round((time.perf_counter() - start_time) * 1000, 2)
        response_time = f"{response_time} milliseconds"

        # Add response time to headers
        if isinstance(response, (JsonResponse, Response)):
            response["X-Response-Time"] = response_time
        elif hasattr(response, 'headers'):
            response.headers["X-Response-Time"] = response_time

        if isinstance(response, JsonResponse):
            # Byte string
            data = response.content

            # Decode the byte string to a regular string
            decoded_data = data.decode('utf-8')

            # Convert the JSON string to a Python dictionary
            data_as_dict = json.loads(decoded_data)

            # Define the empty custom response data
            custom_response = {}

            try:
                if response.status_code >= 400:
                    validate_data = self.is_data_valid(data_as_dict, ["message", "errors"])
                    custom_response = {
                        "status": "failed",
                        "message": validate_data["message"],
                        "data": None,
                        "errors": validate_data.get("errors", []),
                        "meta": self.get_meta(None, response_time)
                    }
                else:
                    validate_data = self.is_data_valid(data_as_dict, ["message", "data"])
                    custom_response = {
                        "status": "succeeded",
                        "message": validate_data["message"],
                        "data": validate_data.get("data"),
                        "errors": [],
                        "meta": self.get_meta(None, response_time)
                    }
                return JsonResponse(custom_response, status=response.status_code)
            except InvalidDataFormatError as error:
                return JsonResponse({
                    "status": "failed",
                    "message": "Invalid response format",
                    "data": None,
                    "errors": [error.error_dict],
                    "meta": self.get_meta(None, response_time)
                }, status=500)

        if isinstance(response, Response):
            throttles = getattr(response, "throttles", [])
            data = response.data
            custom_response = {}

            try:
                if response.status_code >= 400:
                    validate_data = self.is_data_valid(data, ["message", "errors"])
                    custom_response = {
                        "status": "failed",
                        "message": validate_data["message"],
                        "data": None,
                        "errors": validate_data.get("errors", []),
                        "meta": self.get_meta({"rate_limit": throttles}, response_time)
                    }
                else:
                    validate_data = self.is_data_valid(data, ["message", "data"])
                    custom_response = {
                        "status": "succeeded",
                        "message": validate_data["message"],
                        "data": validate_data.get("data"),
                        "errors": [],
                        "meta": self.get_meta({"rate_limit": throttles}, response_time)
                    }
                return JsonResponse(custom_response, status=response.status_code)
            except InvalidDataFormatError as error:
                return JsonResponse({
                    "status": "failed",
                    "message": "Invalid response format",
                    "data": None,
                    "errors": [error.error_dict],
                    "meta": self.get_meta({"rate_limit": throttles}, response_time)
                }, status=500)

        if response.status_code == 429:
            return JsonResponse({
                "status": "failed",
                "message": "Too many requests. Please wait before trying again.",
                "data": None,
                "errors": [{
                    "field": "throttle",
                    "code": "throttle_limit_excide",
                    "message": response.headers.get("Retry-After", "N/A"),
                    "details": None
                }],
                "meta": self.get_meta(None, response_time)
            }, status=response.status_code)

        return response
