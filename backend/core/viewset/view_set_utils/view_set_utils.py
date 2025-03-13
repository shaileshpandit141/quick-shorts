from typing import Union

from django.http import HttpResponseBase  # type: ignore
from rest_framework.request import Request
from rest_framework.response import Response


class ViewSetUtils:
    """TThe model viewset utils is handle the some viewsets utils"""

    def _handle_error_response(
        self, response: Union[Response, HttpResponseBase], data: dict, payload: dict
    ) -> None:
        """Handles error responses."""
        if response.status_code == 404:
            payload.update(
                {
                    "message": data.get("message", "Resource Not Found"),
                    "data": data.get("data", {}),
                    "errors": data.get(
                        "errors", {"detail": "The requested resource was not found"}
                    ),
                }
            )
        else:
            payload.update(
                {
                    "message": data.get("message", "An unexpected error occurred."),
                    "data": data.get("data", {}),
                    "errors": data.get("errors", {}),
                }
            )

    def _handle_success_response(
        self,
        response: Union[Response, HttpResponseBase],
        request: Request,
        data: dict,
        payload: dict,
    ) -> None:
        """Handles successful responses."""
        if response.status_code == 204:
            response.status_code = 200
            payload.update(
                {
                    "message": "The request was successful",
                    "data": {
                        "detail": "The requested resource deletion was successful.",
                        "id": getattr(request, "parser_context", {})
                        .setdefault("kwargs", {})
                        .get("pk", None),
                    },
                }
            )
        else:
            payload.update(
                {
                    "message": "The request was successful",
                    "data": data,
                }
            )

    def _set_custom_headers(
        self, response: Union[Response, HttpResponseBase], request_id: str
    ) -> None:
        """Sets custom headers for tracking request metadata."""
        setattr(
            response,
            "headers",
            {
                **response.headers,
                "X-Request-ID": request_id,
                "X-Status-Code": str(response.status_code),
                "X-Status-Message": (
                    "succeeded" if response.status_code < 400 else "failed"
                ),
            },
        )
