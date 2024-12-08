from typing import TypedDict, Literal, Dict, Union, List, Any, Optional, NotRequired
from rest_framework.response import Response as DRFResponse
from rest_framework import status


class ErrorResponseType(TypedDict):
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


ErrorStatusType = Literal[
    400,   # HTTP_400_BAD_REQUEST - Malformed request or validation error
    401,   # HTTP_401_UNAUTHORIZED - Missing or invalid authentication
    404    # HTTP_404_NOT_FOUND - Resource not found
]


class SuccessResponseType(TypedDict):
    """
    Defines the structure of a standardized success response.

    Attributes:
        message (str): A human-readable message describing the successful result
        data (dict): The response payload containing the requested/created data
        meta (None | dict): Optional metadata about the response (e.g. pagination details)
    """
    message: str
    meta: NotRequired[Dict]
    data: Dict[str, Any] | List[Dict[str, Any]]


SuccessStatusType = Literal[
    200,   # HTTP_200_OK - Request completed successfully
    201,   # HTTP_201_CREATED - New resource created successfully
    204    # HTTP_204_NO_CONTENT - Success but no content returned
]


class Response:
    """
    Utility class that provides standardized formatting for API responses.
    Creates consistent error and success response structures.
    """

    type = DRFResponse

    def __init__(self) -> None:
        pass

    @staticmethod
    def error(
        payload: ErrorResponseType,
        status: ErrorStatusType=status.HTTP_400_BAD_REQUEST,
        template_name: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None) -> DRFResponse:
        """
        Creates a standardized error response structure.

        Args:
            payload (ErrorResponseType): The error details including message and field-level errors
            status (ErrorStatusType): The HTTP status code to return (400, 401, or 404)

        Returns:
            Response: A Django REST framework Response object with formatted error details
        """
        return DRFResponse({
            'status': 'failed',
            'message': payload['message'],
            'errors': payload['errors']
        },
        status=status,
        template_name=template_name,
        headers=headers,
        exception=exception,
        content_type=content_type)

    @staticmethod
    def success(
        payload: SuccessResponseType,
        status: SuccessStatusType = status.HTTP_200_OK,
        template_name: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None) -> DRFResponse:
        """
        Creates a standardized success response structure.

        Args:
            payload (SuccessResponseType): The success details including message, data and metadata
            status (SuccessStatusType): The HTTP status code to return (200, 201, or 204)

        Returns:
            Response: A Django REST framework Response object with formatted success details
        """
        return DRFResponse({
            'status': 'succeeded',
            'message': payload['message'],
            'meta': payload.get('meta', None),
            'data': payload['data']
        },
        status=status,
        template_name=template_name,
        headers=headers,
        exception=exception,
        content_type=content_type)

    @staticmethod
    def method_not_allowed(name: Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']) -> DRFResponse:
        """
        Creates a standardized error response for unsupported HTTP methods.

        Args:
            name (Literal['get', 'post', 'put', 'patch', 'delete']): The HTTP method name that was attempted

        Returns:
            Response: A Django REST framework Response object with formatted error indicating
            the specified HTTP method is not supported on this endpoint
        """
        return Response.error({
            'message': 'Method not allowed',
            'errors': {
                'non_field_errors': [
                    f'{name.upper()} operations are not supported on this endpoint'
                ]
            }
        }, status=status.HTTP_200_OK)  # type: ignore

    @staticmethod
    def options(allowed_methods: List[Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']]) -> DRFResponse:
        """
        Creates a standardized response for OPTIONS requests that describes the API endpoint capabilities.

        Args:
            allowed_methods (List[Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']]):
            List of HTTP methods supported by this endpoint

        Returns:
            DRFResponse: A Django REST framework Response object containing:
            - Supported HTTP methods
            - API description
            - Documentation links
            - Contact information
        """
        return Response.success({
            'message': 'Options request successfully processed',
            'data': {
                'methods': allowed_methods,
                'description': 'This API allows CRUD operations on the resource.',
                'documentation_url': 'https://example.com/docs',
                'terms_of_service': 'https://example.com/terms',
                'contact': {
                    'email': 'support@example.com',
                    'phone': '+1-800-123-4567'
                }
            }
        }, status.HTTP_200_OK)
