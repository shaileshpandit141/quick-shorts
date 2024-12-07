# Django imports
from django.contrib.auth import get_user_model
from django.conf import settings

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import Response, SendEmail, TokenGenerator, add_query_params

User = get_user_model()


class VerifyEmailAPIView(APIView):
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
        email = request.data.get("email", None)

        if not email:
            return Response.error({
                'message': 'Missing email address',
                'errors': {
                    'email': [
                        'Please provide your email address'
                    ]
                }
            }, status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response.error({
                'message': 'Account not found',
                'errors': {
                    'email': [
                        'No account exists with this email address'
                    ]
                }
            }, status.HTTP_400_BAD_REQUEST)

        if not user.is_email_verified:
            # Generate token
            payload = TokenGenerator.generate({"user_id": user.id})
            activate_url = add_query_params(f'{settings.FRONTEND_URL}/auth/verify-email', {
                'token': payload['token'],
                'token_salt': payload['token_salt']
            })

            SendEmail({
                'subject': 'Email Verification Request',
                'emails': {
                    'to_emails': email
                },
                'context': {
                    'user': user,
                    'activate_url': activate_url
                },
                'templates': {
                    'txt': 'users/verify_email_confirm_message.txt',
                    'html': 'users/verify_email_confirm_message.html'
                }
            })
            return Response.success({
                'message': 'Verification email sent',
                'data': {
                    'detail': 'Please check your inbox for the verification email'
                }
            }, status.HTTP_200_OK)
        else:
            return Response.success({
                'message': 'Email already verified',
                'data': {
                    'detail': 'Your email address has already been verified'
                }
            }, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        return Response.options(['POST'])
