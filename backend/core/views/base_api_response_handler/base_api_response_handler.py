import logging
from typing import Any, Self

from rest_framework import status
from rest_framework.response import Response

from .base_api_response_handler_types import (
    TypeData,
    TypeErrorPayload,
    TypeErrors,
    TypeResponsePayload,
    TypeSuccessPayload,
)

logger = logging.getLogger(__name__)


class BaseAPIResponseHandler:
    """
    A handler class for generating standardized API responses.

    Methods:
    --------
    response(payload: TypeResponsePayload, status: int = status.HTTP_200_OK, **kwargs: Any) -> Response:
        Generates a generic API response with the given payload and status.

    success(payload: TypeSuccessPayload, status: int = status.HTTP_200_OK, **kwargs: Any) -> Response:
        Generates a success API response with the given payload and status.

    error(payload: TypeErrorPayload, status: int = status.HTTP_500_INTERNAL_SERVER_ERROR, **kwargs: Any) -> Response:
        Generates an error API response with the given payload and status.
    """

    def response(
        self: Self,
        payload: TypeResponsePayload,
        status: int = status.HTTP_200_OK,
        **kwargs: Any,
    ) -> Response:
        logger.debug(
            f"Generating response with payload: {payload} and status: {status}"
        )

        return Response(
            data={
                "message": payload["message"],
                "data": payload.get("data", {}),
                "errors": payload.get("errors", {}),
            },
            status=status,
            **kwargs,
        )

    def success(
        self: Self,
        payload: TypeSuccessPayload,
        status: int = status.HTTP_200_OK,
        **kwargs: Any,
    ) -> Response:
        logger.info(f"Success response with payload: {payload} and status: {status}")
        return self.response(
            payload={**payload, "errors": {}},
            status=status,
            **kwargs,
        )

    def error(
        self: Self,
        payload: TypeErrorPayload,
        status: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        **kwargs: Any,
    ) -> Response:
        logger.error(f"Error response with payload: {payload} and status: {status}")
        return self.response(
            payload={
                "message": payload["message"],
                "data": {},
                "errors": payload["errors"],
            },
            status=status,
            **kwargs,
        )

    def handle_success(
        self, message: str, data: TypeData, status: int = status.HTTP_200_OK
    ) -> Response:
        logger.info(
            f"Handling success with message: {message}, data: {data}, status: {status}"
        )
        return self.success({"message": message, "data": data}, status=status)

    def handle_error(
        self,
        message: str,
        errors: TypeErrors,
        status: int = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        logger.warning(
            f"Handling error with message: {message}, errors: {errors}, status: {status}"
        )
        return self.error({"message": message, "errors": errors}, status=status)

    def handle_delete(self) -> Response:
        logger.info("Handling DELETE request")
        response = Response({}, status=status.HTTP_204_NO_CONTENT)
        setattr(
            response,
            "headers",
            {
                **response.headers,
                "Content-Length": "0",
            },
        )
        return response
