# Django imports
from django.contrib.auth import get_user_model
from django.conf import settings

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import (
    Response,
    SendEmail,
    TokenGenerator,
    FieldValidator,
    add_query_params
)

User = get_user_model()


class ForgotPasswordAPIView(APIView):
    """
    API endpoint for handling forgot password functionality.

    This view handles password reset requests by sending reset emails to verified users.
    It validates the email address, checks account verification status, and sends password
    reset instructions via email.

    Methods:
        get: Not supported
        post: Process forgot password request and send reset email
        put: Not supported
        patch: Not supported
        delete: Not supported
        options: Returns allowed HTTP methods

    Attributes:
        permission_classes (list): Allows access to any user (authenticated or not)
        throttle_classes (list): Applies rate limiting for anonymous requests
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """GET method not supported."""
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        """
        Process forgot password request and send reset email.

        Validates the submitted email address, checks if the associated account exists
        and is verified. For verified accounts, generates a password reset token and
        sends reset instructions via email.

        Args:
            request: HTTP request object containing email address in request.data

        Returns:
            Response: JSON response with appropriate success/error message and status code
                - 200 OK: Reset email sent successfully
                - 400 Bad Request: Invalid email, account not found, or unverified account
        """
        # Validate required fields
        validator = FieldValidator(request.data, ['email'])

        if not validator.is_valid():
            return Response.error({
                'message': 'Missing email address',
                'errors': validator.errors
            }, status.HTTP_400_BAD_REQUEST)

        # Check if user exists
        try:
            user = User.objects.get(email=validator.get('email'))
        except User.DoesNotExist:
            return Response.error({
                'message': 'Account not found',
                'errors': {
                    'email': [
                        'No account exists with this email address'
                    ]
                }
            }, status.HTTP_400_BAD_REQUEST)

        # Process request for verified users
        if user.is_verified:
            # Generate reset token
            payload = TokenGenerator.generate({"user_id": user.id})
            active_url = add_query_params(f'{settings.FRONTEND_URL}/auth/verify-email', {
                'token': payload['token'],
                'token_salt': payload['token_salt']
            })

            # Send reset email
            SendEmail({
                'subject': 'Password Reset Request',
                'emails': {
                    'to_emails': [user.email]
                },
                'context': {
                    'user': user,
                    'active_url': active_url
                },
                'templates': {
                    'txt': 'users/forgot_password/confirm_message.txt',
                    'html': 'users/forgot_password/confirm_message.html'
                }
            })
            return Response.success({
                'message': 'Forgot password email sent',
                'data': {
                    'detail': 'Please check your inbox for the Forgot password'
                }
            }, status.HTTP_200_OK)
        else:
            return Response.error({
                "message": "Please verify your email to continue.",
                "errors": {
                    "detail": [
                        "You must verify your email address to access this resource."
                    ]
                }
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs) -> Response.type:
        """PUT method not supported."""
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """PATCH method not supported."""
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        """DELETE method not supported."""
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """Return allowed HTTP methods for this endpoint."""
        return Response.options(['POST'])
