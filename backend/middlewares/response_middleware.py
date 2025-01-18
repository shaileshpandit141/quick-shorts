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
            "details": {"help": details}
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
        meta = {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "response_time": response_time,
            "documentation_url": "N/A",
        }
        if custom_meta:
            meta.update(custom_meta)
        return meta

    def create_response_dict(
        self,
        success: bool,
        validate_data: DataType,
        throttles: list,
        response_time: str
    ) -> dict:
        return {
            "status": "succeeded" if success else "failed",
            "message": validate_data["message"],
            "data": validate_data.get("data") if success else None,
            "errors": validate_data.get("errors", []) if not success else [],
            "meta": self.get_meta({"rate_limit": throttles}, response_time)
        }

    def handle_response(
        self,
        data: DataType | None,
        response: Any,
        throttles: list,
        response_time: str
    ) -> JsonResponse:
        try:
            success = response.status_code < 400
            expected_keys = ["message", "data"] if success else ["message", "errors"]
            validate_data = self.is_data_valid(data, expected_keys)
            custom_response = self.create_response_dict(
                success,
                validate_data,
                throttles,
                response_time
            )
            return JsonResponse(custom_response, status=response.status_code)
        except InvalidDataFormatError as error:
            return JsonResponse({
                "status": "failed",
                "message": "Invalid response format",
                "data": None,
                "errors": [error.error_dict],
                "meta": self.get_meta({"rate_limit": throttles}, response_time)
            }, status=500)

    def is_data_valid(self, data: DataType | None, expected_keys: List[str]) -> DataType:
        if not data or not isinstance(data, dict):
            raise InvalidDataFormatError(
                message="Response data must be a valid dictionary format.",
                code="invalid_format",
                details="The response data is either missing or not in dictionary format"
            )

        if sorted(data.keys()) != sorted(expected_keys):
            raise InvalidDataFormatError(
                message="Response data is missing required fields or contains invalid fields.",
                code="invalid_keys",
                details=f"Expected fields: {
                    ', '.join(expected_keys)}. Received fields: {', '.join(data.keys())}"
            )

        return data

    def __call__(self, request):
        start_time = time.perf_counter()
        response = self.get_response(request)
        response_time = f"{round(time.perf_counter() - start_time, 5)} seconds"
        throttles = getattr(response, "throttles", [])

        if isinstance(response, (JsonResponse, Response)):
            response["X-Response-Time"] = response_time
        elif hasattr(response, 'headers'):
            response.headers["X-Response-Time"] = response_time

        if isinstance(response, JsonResponse):
            data = json.loads(response.content.decode('utf-8'))
            return self.handle_response(data, response, throttles, response_time)

        if isinstance(response, Response):
            return self.handle_response(response.data, response, throttles, response_time)

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
                "meta": self.get_meta({"rate_limit": throttles}, response_time)
            }, status=response.status_code)

        return response
