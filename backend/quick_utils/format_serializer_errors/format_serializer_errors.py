from typing import Any
from ..types import ErrorsType


def format_serializer_errors(errors: Any) -> ErrorsType:
    """Format Django Rest Framework serializer errors into a structured list."""

    formatted_errors: ErrorsType = []

    def append_error(field, code="invalid", message="An error occurred", details=None):
        """Helper function to append an error to the formatted_errors list."""

        formatted_errors.append({
            "field": field,
            "code": code,
            "message": message,
            "details": details,
        })

    for field, error_messages in errors.items():
        if isinstance(error_messages, list):
            for message in error_messages:
                if isinstance(message, dict):
                    append_error(
                        field,
                        code=message.get("code", "invalid"),
                        message=message.get("message", "An error occurred"),
                        details=message.get("details", None),
                    )
                else:
                    append_error(field, message=str(message))
        elif isinstance(error_messages, dict):
            append_error(
                field,
                code=error_messages.get("code", "invalid"),
                message=error_messages.get("message", "An error occurred"),
                details=error_messages.get("details", None),
            )
        else:
            append_error(field, message=str(error_messages))

    return formatted_errors
