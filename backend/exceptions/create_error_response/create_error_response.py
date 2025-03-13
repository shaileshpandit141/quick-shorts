import logging
from typing import Any
from core.response import Response

logger = logging.getLogger(__name__)


def create_error_response(
    message: str, errors: Any, status: int | None = None
) -> Response:
    """Helper function to create error response"""
    error_details = {"detail": "Oops! unknown error occurred. Please try again later"}

    try:
        errors_tuple = errors.args
        if len(errors_tuple) > 0 and isinstance(errors_tuple[0], dict):
            error_details = errors_tuple[0]
        elif hasattr(errors, "detail"):
            error_details["detail"] = errors.detail
        elif hasattr(errors, "message"):
            error_details["detail"] = errors.message
        elif isinstance(errors, dict):
            error_details = errors
        elif isinstance(errors, str):
            error_details["detail"] = errors
        else:
            error_details["detail"] = str(errors)
    except Exception as error:
        logger.error(f"Error occurred while processing error details: {str(error)}")
        error_details = {"detail": str(error)}

    return Response(
        {
            "message": message,
            "data": {},
            "errors": error_details,
        },
        status,
    )
