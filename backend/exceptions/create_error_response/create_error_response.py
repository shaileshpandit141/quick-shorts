from quick_utils.response import Response


def create_error_response(
    message, code, field="none", error_message=None, details=None
) -> Response:
    """Helper function to create error response"""
    return Response(
        {
            "message": message,
            "errors": [
                {
                    "field": field,
                    "code": code,
                    "message": error_message or message,
                    "details": details,
                }
            ],
        }
    )
