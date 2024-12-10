# Django imports
from django.contrib.auth import get_user_model

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework_simplejwt.views import TokenRefreshView

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import Response, TokenGenerator, FieldValidator

User = get_user_model()


class VerifyAccountConfirmAPIView(APIView):
    """
    API View for verifying user accounts via email confirmation.
    Handles the verification of email tokens and updates user verification status.

    Attributes:
        permission_classes: Allows any user (authenticated or not) to access the endpoint
        throttle_classes: Applies rate limiting for anonymous users
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """Handle GET request - not allowed for this endpoint"""
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        """
        Handle POST request for email verification

        Args:
            request: HTTP request object containing token and token_salt

        Returns:
            Response object with success/error message and appropriate status code
        """
        # Validate required fields
        clean_data = FieldValidator(request.data, ['token', 'token_salt'])
        if not clean_data.is_valid:
            return Response.error({
                'message': 'Invalid request',
                'errors': clean_data.get_errors()
            }, status.HTTP_400_BAD_REQUEST)

        try:
            # Decode verification token
            data = TokenGenerator.decode(
                clean_data.get('token'),
                clean_data.get('token_salt')
            )
            user = User.objects.get(id=data["user_id"])

            # Check if already verified
            if user.is_verified:
                return Response.success({
                    'message': 'Email already verified',
                    'data': {
                        'detail': 'Email already verified.'
                    }
                }, status.HTTP_200_OK)

            # Update verification status
            user.is_verified = True
            user.save()
            return Response.success({
                'message': 'Email verified successfully',
                'data': {
                    'detail': 'Email verified successfully'
                }
            }, status.HTTP_200_OK)

        except ValueError as error:
            return Response.error({
                'message': 'Invalid token',
                'errors': {
                    'non_field_errors': [str(error)]
                }
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs) -> Response.type:
        """Handle PUT request - not allowed for this endpoint"""
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """Handle PATCH request - not allowed for this endpoint"""
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        """Handle DELETE request - not allowed for this endpoint"""
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """Return allowed HTTP methods for this endpoint."""
        return Response.options(['POST'])
