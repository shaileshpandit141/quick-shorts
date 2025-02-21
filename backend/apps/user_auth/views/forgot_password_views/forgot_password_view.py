from django.conf import settings
from django.contrib.auth import get_user_model
from permissions import AllowAny
from quick_utils.send_email import SendEmail
from limited_time_token_handler import LimitedTimeTokenGenerator
from quick_utils.views import APIView, Response
from throttling import AuthRateThrottle
from utils import FieldValidator, add_query_params

User = get_user_model()


class ForgotPasswordView(APIView):
    """API endpoint for handling forgot password functionality."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Process forgot password request and send reset email."""

        # Validate required fields
        validator = FieldValidator(request.data, ["email"])

        if not validator.is_valid():
            return self.response(
                {"message": "Missing email address", "errors": validator.errors},
                self.status.HTTP_400_BAD_REQUEST,
            )
        # Check if user exists
        try:
            user = User.objects.get(email=validator.get("email"))
        except User.DoesNotExist:
            return self.response(
                {
                    "message": "Account not found",
                    "errors": [
                        {
                            "field": "email",
                            "code": "invalid_email",
                            "message": "No account exists with this email address",
                            "details": None,
                        }
                    ],
                },
                self.status.HTTP_400_BAD_REQUEST,
            )

        # Process request for verified users
        if getattr(user, "is_verified", False):
            # Generate reset token
            generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
            token = generator.generate()
            if token is None:
                return self.response(
                    {
                        "message": "Token generation failed",
                        "errors": [
                            {
                                "field": "none",
                                "code": "token_generation_failed",
                                "message": "Failed to generate token",
                                "details": None,
                            }
                        ],
                    },
                    self.status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            active_url = add_query_params(
                f"{settings.FRONTEND_URL}/auth/verify-email", {"token": token}
            )

            # Send reset email
            SendEmail(
                {
                    "subject": "Password Reset Request",
                    "emails": {"to_emails": [user.email]},
                    "context": {"user": user, "active_url": active_url},
                    "templates": {
                        "txt": "users/forgot_password/confirm_message.txt",
                        "html": "users/forgot_password/confirm_message.html",
                    },
                }
            )
            return self.response(
                {
                    "message": "Forgot password email sent",
                    "data": {
                        "detail": "Please check your inbox for the Forgot password"
                    },
                },
                self.status.HTTP_200_OK,
            )
        else:
            return self.response(
                {
                    "message": "Please verify your email to continue.",
                    "errors": [
                        {
                            "field": "none",
                            "code": "account_not_varified",
                            "message": "You must verify your account to access this resource.",
                            "details": {"account_verified": False},
                        }
                    ],
                },
                self.status.HTTP_400_BAD_REQUEST,
            )
