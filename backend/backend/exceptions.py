from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _

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
        error_context = {
            'status': _('error'),
            'message': _('Authentication Failed'),
            'error': {
                'detail': _('Authentication credentials were not provided or invalid.')
            }
        }
        return Response(error_context, status=status.HTTP_401_UNAUTHORIZED)

    # Handle AuthenticationFailed exceptions
    if isinstance(exc, AuthenticationFailed):
        # Format custom error response for invalid authentication
        error_context = {
            'status': _('error'),
            'message': _('Access Denied'),
            'error': {
                'detail': _('Please provide valid authentication credentials.'),
                'refresh_token': _('Provided refresh token has expired.')
            }
        }
        return Response(error_context, status=status.HTTP_401_UNAUTHORIZED)

    # Return default response for any other exceptions
    return response
