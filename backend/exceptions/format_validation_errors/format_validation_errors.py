from typing import Any


def format_validation_errors(detail) -> list[Any]:
    """Helper function to format validation errors"""
    error_details = []
    if isinstance(detail, dict):
        for field, messages in detail.items():
            if field == "non_field_errors":
                field = "none"
            if isinstance(messages, list):
                for message in messages:
                    error_details.append(
                        {
                            "field": field,
                            "code": getattr(message, "code", "validation_error"),
                            "message": str(message),
                            "details": None,
                        }
                    )
            else:
                error_details.append(
                    {
                        "field": field,
                        "code": getattr(messages, "code", "validation_error"),
                        "message": str(messages),
                        "details": None,
                    }
                )
    else:
        error_details.append(
            {
                "field": "none",
                "code": "validation_error",
                "message": str(detail),
                "details": None,
            }
        )
    return error_details
