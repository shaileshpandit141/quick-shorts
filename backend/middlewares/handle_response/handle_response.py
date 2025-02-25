from logging import getLogger
from typing import Any

from django.http import JsonResponse

from ..add_response_headers import add_response_headers
from ..add_throttle_details_in_header import add_throttle_details_in_header
from ..create_response_dict import create_response_dict
from ..get_meta import get_meta
from ..invalid_data_format_error import InvalidDataFormatError
from ..is_data_valid import is_data_valid
from ..types import DataType

# Configure logger
logger = getLogger(__name__)


# Response Processing
def handle_response(
    data: DataType | None,
    response: Any,
    throttles: list,
    response_time: str,
    request: Any,
    request_id: str,
) -> JsonResponse:
    try:
        success = response.status_code < 400
        expected_keys = ["message", "data"] if success else ["message", "errors"]
        validate_data = is_data_valid(data, expected_keys)
        custom_response = create_response_dict(
            success,
            validate_data,
            throttles,
            response_time,
            request_id,
            response.status_code,
        )

        json_response = JsonResponse(custom_response, status=response.status_code)
        add_response_headers(
            json_response,
            {
                "X-Processing-Time": response_time,
                "X-Request-ID": request_id,
                "X-Status-Code": str(response.status_code),
            },
        )
        add_throttle_details_in_header(json_response, throttles)
        logger.info(f"Request {request_id} processed successfully")
        return json_response
    except InvalidDataFormatError as error:
        logger.error(
            f"Invalid data format error for request {request_id}: {str(error)}"
        )
        json_response = JsonResponse(
            {
                "status": "failed",
                "status_code": 500,
                "message": "Invalid response format",
                "data": None,
                "errors": [error.error_dict],
                "meta": get_meta({"rate_limit": throttles}, response_time, request_id),
            },
            status=500,
        )
        add_response_headers(
            json_response,
            {
                "X-Processing-Time": response_time,
                "X-Request-ID": request_id,
                "X-Status-Code": "500",
            },
        )
        add_throttle_details_in_header(json_response, throttles)
        return json_response
