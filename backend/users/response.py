from typing import TypedDict, Literal, Dict, Union, List
from rest_framework.response import Response as DRFResponse
from rest_framework import status


class TypedErrorResponse(TypedDict):
    """
    Defines the structure of a standardized error response.

    Attributes:
        message (str): A human-readable error message explaining what went wrong
        errors (Dict[str, Union[List[str], str]]): A dictionary containing field-level validation errors.
            The keys are field names and values can be either a single error string
            or a list of error strings related to that field.
    """
    message: str
    errors: Dict[str, Union[List[str], str]]


TypedErrorStatus = Literal[
    400,   # HTTP_400_BAD_REQUEST - Malformed request or validation error
    401,   # HTTP_401_UNAUTHORIZED - Missing or invalid authentication
    404    # HTTP_404_NOT_FOUND - Resource not found
]


class TypedSuccessResponse(TypedDict):
    """
    Defines the structure of a standardized success response.

    Attributes:
        message (str): A human-readable message describing the successful result
        data (dict): The response payload containing the requested/created data
        meta (None | dict): Optional metadata about the response (e.g. pagination details)
    """
    message: str
    data: dict
    meta: None | dict


TypedSuccessStatus = Literal[
    200,   # HTTP_200_OK - Request completed successfully
    201,   # HTTP_201_CREATED - New resource created successfully
    204    # HTTP_204_NO_CONTENT - Success but no content returned
]


class Response:
    """
    Utility class that provides standardized formatting for API responses.
    Creates consistent error and success response structures.
    """
    def __init__(self):
        pass

    @staticmethod
    def error(
        payload: TypedErrorResponse,
        status: TypedErrorStatus=status.HTTP_400_BAD_REQUEST) -> DRFResponse:
        """
        Creates a standardized error response structure.

        Args:
            payload (TypedErrorResponse): The error details including message and field-level errors
            status (TypedErrorStatus): The HTTP status code to return (400, 401, or 404)

        Returns:
            DRFResponse: A Django REST framework Response object with formatted error details
        """
        return DRFResponse({
            'status': 'failed',
            'message': payload['message'],
            'errors': payload['errors']
        }, status=status)

    @staticmethod
    def success(
        payload: TypedSuccessResponse,
        status: TypedSuccessStatus = status.HTTP_200_OK) -> DRFResponse:
        """
        Creates a standardized success response structure.

        Args:
            payload (TypedSuccessResponse): The success details including message, data and metadata
            status (TypedSuccessStatus): The HTTP status code to return (200, 201, or 204)

        Returns:
            DRFResponse: A Django REST framework Response object with formatted success details
        """
        return DRFResponse({
            'status': 'succeeded',
            'message': payload['message'],
            'data': payload['data'],
            'meta': payload['meta']
        }, status=status)
