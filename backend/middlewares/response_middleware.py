from typing import Any, Dict, List, NotRequired, Optional, TypedDict
import json
import time
import uuid
import logging
from datetime import datetime  # type: ignore
from django.http import JsonResponse
from rest_framework.response import Response
from last_request_log.models import LastRequestLog
from utils import get_client_ip

# Configure logger
logger = logging.getLogger(__name__)

# Custom Exceptions
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


# Type Definitions
class DataType(TypedDict):
    message: str
    data: NotRequired[Dict[str, Any]]
    errors: NotRequired[List[Dict[str, Any]]]


# Main Middleware Class
class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logger

    # Meta Data Helpers
    def get_meta(
        self,
        custom_meta: Optional[Dict[str, Any]] = None,
        response_time: str = "N/A",
        request_id: str = "N/A"
    ) -> Dict[str, Any]:
        meta = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "response_time": response_time,
            "documentation_url": "N/A"
        }
        if custom_meta:
            meta.update(custom_meta)
        return meta

    def create_response_dict(
        self,
        success: bool,
        validate_data: DataType,
        throttles: list,
        response_time: str,
        request_id: str,
        status_code: int = 200
    ) -> dict:
        return {
            "status": "succeeded" if success else "failed",
            "status_code": status_code,
            "message": validate_data["message"],
            "data": validate_data.get("data") if success else None,
            "errors": validate_data.get("errors", []) if not success else [],
            "meta": self.get_meta({"rate_limit": throttles}, response_time, request_id)
        }

    # Logging Functions
    def log_request(self, request: Any, response_time: str, success: bool, is_api_request: bool):
        objects = getattr(LastRequestLog, "objects", None)
        if objects is not None:
            try:
                client_ip = get_client_ip(request)
                log_entry = objects.filter(ip=client_ip).first()
                if log_entry:
                    log_entry.user = request.user.email if request.user.is_authenticated else None
                    log_entry.path = request.path
                    log_entry.method = request.method
                    log_entry.timestamp = datetime.utcnow()
                    log_entry.response_time = response_time
                    log_entry.is_authenticated = request.user.is_authenticated
                    log_entry.is_api_request = is_api_request
                    log_entry.is_request_success = success
                    log_entry.save()
                else:
                    objects.create(
                        user=request.user.email if request.user.is_authenticated else None,
                        path=request.path,
                        method=request.method,
                        ip=client_ip,
                        timestamp=datetime.utcnow(),
                        response_time=response_time,
                        is_authenticated=request.user.is_authenticated,
                        is_api_request=is_api_request,
                        is_request_success=success
                    )
                self.logger.info(f"Request logged - Path: {request.path}, Method: {request.method}, Success: {success}")
            except Exception as error:
                self.logger.error(f"Error logging request: {str(error)}")

    # Header Management
    def add_response_headers(self, response: Any, headers: Dict[str, str]) -> None:
        try:
            if isinstance(response, (JsonResponse, Response)):
                for key, value in headers.items():
                    response[key] = value
            elif hasattr(response, 'headers'):
                for key, value in headers.items():
                    response.headers[key] = value
            self.logger.debug(f"Added headers: {headers}")
        except Exception as e:
            self.logger.error(f"Error adding headers: {str(e)}")

    def add_throttle_details_to_header(self, response: Any, throttles: List[Dict[str, Any]]) -> None:
        if not throttles:
            return

        try:
            headers = {}
            for throttle in throttles:
                if not all(key in throttle for key in ['type', 'limit', 'remaining', 'reset_time', 'retry_after']):
                    continue

                headers.update({
                    f"X-RateLimit-{throttle['type']}-Limit": str(throttle['limit']),
                    f"X-RateLimit-{throttle['type']}-Remaining": str(throttle['remaining']),
                    f"X-RateLimit-{throttle['type']}-Reset": str(throttle['reset_time']),
                    f"X-RateLimit-{throttle['type']}-Retry-After": str(throttle['retry_after'])
                })

            if headers:
                self.add_response_headers(response, headers)
                self.logger.debug(f"Added throttle headers: {headers}")
        except Exception as e:
            self.logger.error(f"Error adding throttle details: {str(e)}")

    # Response Processing
    def handle_response(
        self,
        data: DataType | None,
        response: Any,
        throttles: list,
        response_time: str,
        request: Any,
        request_id: str
    ) -> JsonResponse:
        try:
            success = response.status_code < 400
            expected_keys = ["message", "data"] if success else ["message", "errors"]
            validate_data = self.is_data_valid(data, expected_keys)
            custom_response = self.create_response_dict(
                success,
                validate_data,
                throttles,
                response_time,
                request_id,
                response.status_code
            )

            self.log_request(request, response_time, success, True)
            json_response = JsonResponse(custom_response, status=response.status_code)
            self.add_response_headers(json_response, {
                "X-Processing-Time": response_time,
                "X-Request-ID": request_id,
                "X-Status-Code": str(response.status_code)
            })
            self.add_throttle_details_to_header(json_response, throttles)
            self.logger.info(f"Request {request_id} processed successfully")
            return json_response
        except InvalidDataFormatError as error:
            self.logger.error(f"Invalid data format error for request {request_id}: {str(error)}")
            json_response = JsonResponse({
                "status": "failed",
                "status_code": 500,
                "message": "Invalid response format",
                "data": None,
                "errors": [error.error_dict],
                "meta": self.get_meta({"rate_limit": throttles}, response_time, request_id)
            }, status=500)
            self.add_response_headers(json_response, {
                "X-Processing-Time": response_time,
                "X-Request-ID": request_id,
                "X-Status-Code": "500"
            })
            self.add_throttle_details_to_header(json_response, throttles)
            return json_response

    # Data Validation
    def is_data_valid(self, data: DataType | None, expected_keys: List[str]) -> DataType:
        if not data or not isinstance(data, dict):
            self.logger.error("Invalid data format: Data is missing or not a dictionary")
            raise InvalidDataFormatError(
                message="Response data must be a valid dictionary format.",
                code="invalid_format",
                details="The response data is either missing or not in dictionary format"
            )

        if sorted(data.keys()) != sorted(expected_keys):
            self.logger.error(f"Invalid keys: Expected {expected_keys}, got {data.keys()}")
            raise InvalidDataFormatError(
                message="Response data is missing required fields or contains invalid fields.",
                code="invalid_keys",
                details=f"Expected fields: {', '.join(expected_keys)}. Received fields: {', '.join(data.keys())}"
            )

        return data

    # Main Entry Point
    def __call__(self, request):
        start_time = time.perf_counter()
        request_id = str(uuid.uuid4())
        self.logger.info(f"Processing request {request_id} - {request.method} {request.path}")

        try:
            response = self.get_response(request)
            response_time = f"{round(time.perf_counter() - start_time, 5)} seconds"
            throttles = getattr(response, "throttles", [])

            if isinstance(response, JsonResponse):
                data = json.loads(response.content.decode('utf-8'))
                return self.handle_response(
                    data,
                    response,
                    throttles,
                    response_time,
                    request,
                    request_id
                )

            if isinstance(response, Response):
                return self.handle_response(
                    response.data,
                    response,
                    throttles,
                    response_time,
                    request,
                    request_id
                )

            if response.status_code == 429:
                self.logger.warning(f"Rate limit exceeded for request {request_id}")
                json_response = JsonResponse({
                    "status": "failed",
                    "status_code": 429,
                    "message": "Too many requests. Please wait before trying again.",
                    "data": None,
                    "errors": [{
                        "field": "throttle",
                        "code": "throttle_limit_excide",
                        "message": response.headers.get("Retry-After", "N/A"),
                        "details": None
                    }],
                    "meta": self.get_meta({"rate_limit": throttles}, response_time, request_id)
                }, status=response.status_code)
                self.add_response_headers(json_response, {
                    "X-Processing-Time": response_time,
                    "X-Request-ID": request_id,
                    "X-Status-Code": "429"
                })
                self.add_throttle_details_to_header(json_response, throttles)
                return json_response

            # Log non-API requests before returning response
            success = response.status_code < 400
            self.log_request(request, response_time, success, False)
            self.add_response_headers(response, {
                "X-Request-ID": request_id,
                "X-Status-Code": str(response.status_code)
            })
            self.add_throttle_details_to_header(response, throttles)
            return response

        except Exception as error:
            self.logger.error(f"Unhandled error processing request {request_id}: {str(error)}")
            raise
