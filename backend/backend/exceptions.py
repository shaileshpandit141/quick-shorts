from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework import status
from utils import Response

def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST framework that provides formatted error responses.

    This handler extends the default DRF exception handler to provide more detailed and
    consistent error messages for authentication-related exceptions.

    Args:
        exc (Exception): The caught exception
        context (dict): Additional context information about the exception

    Returns:
        Response: A REST framework Response object with formatted error details
    """
    # Get the standard error response from DRF's default handler
    response = exception_handler(exc, context)

    # Handle NotAuthenticated exceptions
    if isinstance(exc, NotAuthenticated):
        # Format custom error response for missing authentication
        return Response.error({
            'message': 'Authentication Failed',
            'errors': {
                'non_field_errors': [
                    'Authentication credentials were not provided or invalid.'
                ]
            }
        }, status.HTTP_401_UNAUTHORIZED)

    # Handle AuthenticationFailed exceptions
    if isinstance(exc, AuthenticationFailed):
        # Format custom error response for invalid authentication
        return Response.error({
            'message': 'Access Denied',
            'errors': {
                'non_field_errors': [
                    'Please provide valid authentication credentials.'
                ]
            }
        }, status.HTTP_401_UNAUTHORIZED)

    # Return default response for any other exceptions
    return response
