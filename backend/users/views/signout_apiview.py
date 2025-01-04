# Django REST framework imports
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import Response, FieldValidator


class SignoutAPIView(APIView):
    """API view for user sign out functionality.

    This view handles user sign out by blacklisting their JWT refresh token.
    Only POST method is supported. All other HTTP methods return 405 Method Not Allowed.
    Requires user authentication and implements rate limiting.
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """GET method not supported for sign out."""
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        """Handle user sign out by blacklisting their refresh token.

        Args:
            request: HTTP request object containing refresh_token in request.data

        Returns:
            Response object with success/error message

        Raises:
            ValidationError: If refresh_token is missing or invalid
        """
        # Validate the refresh token is present in request data
        clean_data = FieldValidator(request.data, ['refresh_token'])
        if not clean_data.is_valid():
            return Response.error({
                'message': 'Invalid Request',
                'errors': clean_data.get_errors()
            })

        try:
            # Get and blacklist the refresh token
            token = RefreshToken(clean_data.get('refresh_token'))
            token.blacklist()

            return Response.success({
                'message': 'Sign out successful',
                'data': {
                    'detail': 'Token successfully blacklisted.'
                }
            }, status.HTTP_200_OK)

        except TokenError:
            return Response.error({
                'message': 'Invalid token',
                'errors': {
                    'non_field_errors': ['Token is invalid or expired']
                }
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs) -> Response.type:
        """PUT method not supported for sign out."""
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """PATCH method not supported for sign out."""
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        """DELETE method not supported for sign out."""
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """Return allowed HTTP methods for this endpoint."""
        return Response.options(['POST'])
