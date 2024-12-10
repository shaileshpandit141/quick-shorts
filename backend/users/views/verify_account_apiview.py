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
    add_query_params,
    FieldValidator
)

User = get_user_model()


class VerifyAccountAPIView(APIView):
    """
    API View for handling account email verification.

    This view provides endpoints for resending verification emails to unverified user accounts.
    It validates the email address existence and current verification status before sending
    a new verification email.

    Methods:
        post: Process an email verification resend request
        get: Not allowed - returns 405
        put: Not allowed - returns 405
        patch: Not allowed - returns 405
        delete: Not allowed - returns 405
        options: Returns allowed methods

    Attributes:
        permission_classes (list): [AllowAny] - Allows unauthenticated access
        throttle_classes (list): [AnonRateThrottle] - Rate limits anonymous requests
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """GET method not supported."""
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        """
        Process a request to resend an account verification email.

        Validates the provided email address and checks if the associated account exists
        and needs verification. If valid, generates a new verification token and sends
        a verification email to the user.

        Args:
            request (Request): HTTP request object containing 'email' in request.data
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            Response: JSON response with appropriate status code
                - 200: Email sent successfully or account already verified
                - 400: Invalid/missing email or account not found
        """
        # Validate required email field
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

        if not user.is_verified:
            # Generate verification token and URL
            payload = TokenGenerator.generate({"user_id": user.id})
            activate_url = add_query_params(f'{settings.FRONTEND_URL}/auth/verify-email', {
                'token': payload['token'],
                'token_salt': payload['token_salt']
            })

            # Send verification email
            SendEmail({
                'subject': 'Account Verification Request',
                'emails': {
                    'to_emails': [clean_data.get('email')]
                },
                'context': {
                    'user': user,
                    'activate_url': activate_url
                },
                'templates': {
                    'txt': 'users/verify_account/confirm_message.txt',
                    'html': 'users/verify_account/confirm_message.html'
                }
            })
            return Response.success({
                'message': 'Account verification email sent',
                'data': {
                    'detail': 'Please check your inbox for the account verification.'
                }
            }, status.HTTP_200_OK)
        else:
            return Response.success({
                'message': 'Account already verified',
                'data': {
                    'detail': 'Your account has already been verified.'
                }
            }, status.HTTP_200_OK)

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
