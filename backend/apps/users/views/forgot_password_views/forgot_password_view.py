# Django imports
from django.contrib.auth import get_user_model
from django.conf import settings

# Local imports
from quick_utils.views import APIView, Response
from permissions import AllowAny
from throttling import AuthRateThrottle
from utils import FieldValidator, add_query_params
from quick_utils.send_email import SendEmail
from quick_utils.token_generator import TokenGenerator

User = get_user_model()


class ForgotPasswordView(APIView):
    """API endpoint for handling forgot password functionality."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Process forgot password request and send reset email."""

        # Validate required fields
        validator = FieldValidator(request.data, ['email'])

        if not validator.is_valid():
            return self.response({
                "message": "Missing email address",
                "errors": validator.errors
            }, self.status.HTTP_400_BAD_REQUEST)
        # Check if user exists
        try:
            user = User.objects.get(email=validator.get('email'))
        except User.DoesNotExist:
            return self.response({
                "message": "Account not found",
                "errors": [{
                    "field": "email",
                    "code": "invalid_email",
                    "message": "No account exists with this email address",
                    "details": None,
                }]
            }, self.status.HTTP_400_BAD_REQUEST)

        # Process request for verified users
        if user.is_verified:
            # Generate reset token
            payload = TokenGenerator.generate({"user_id": user.id})
            active_url = add_query_params(f"{settings.FRONTEND_URL}/auth/verify-email", {
                "token": payload["token"],
                "token_salt": payload["token_salt"]
            })

            # Send reset email
            SendEmail({
                "subject": "Password Reset Request",
                "emails": {
                    "to_emails": [user.email]
                },
                "context": {
                    "user": user,
                    "active_url": active_url
                },
                "templates": {
                    "txt": "users/forgot_password/confirm_message.txt",
                    "html": "users/forgot_password/confirm_message.html"
                }
            })
            return self.response({
                "message": "Forgot password email sent",
                "data": {
                    "detail": "Please check your inbox for the Forgot password"
                },
            }, self.status.HTTP_200_OK)
        else:
            return self.response({
                "message": "Please verify your email to continue.",
                "errors": [{
                    "field": "none",
                    "code": "account_not_varified",
                    "message": "You must verify your account to access this resource.",
                    "details": {
                        "account_verified": False
                    }
                }]
            }, self.status.HTTP_400_BAD_REQUEST)
