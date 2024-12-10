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
    View for resending account verification emails.

    Handles requests to resend verification emails for unverified accounts.
    Validates email existence and verification status before sending.

    Methods:
        post: Process email verification resend request

    Attributes:
        permission_classes: Allow any user to access
        throttle_classes: Rate limiting for anonymous requests only
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        """
        Process request to resend verification email.

        Validates email existence and current verification status
        before sending new verification email.

        Args:
            request: HTTP request containing email address

        Returns:
            Response indicating success or error status
        """
        clean_data = FieldValidator(request.data, ['email'])

        if not clean_data.is_valid():
            return Response.error({
                'message': 'Missing email address',
                'errors': clean_data.get_errors()
            }, status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=clean_data.get('email'))
        except User.DoesNotExist:
            return Response.error({
                'message': 'Account not found',
                'errors': {
                    'email': [
                        'No account exists with this email address'
                    ]
                }
            }, status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            # Generate token
            payload = TokenGenerator.generate({"user_id": user.id})
            active_url = add_query_params(f'{settings.FRONTEND_URL}/auth/verify-email', {
                'token': payload['token'],
                'token_salt': payload['token_salt']
            })
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
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """OPTIONS method not supported."""
        return Response.options(['POST'])