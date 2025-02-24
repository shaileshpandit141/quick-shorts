from django.conf import settings
from django.contrib.auth import get_user_model
from limited_time_token_handler import LimitedTimeTokenGenerator

from permissions import AllowAny
from quick_utils.send_email import SendEmail
from quick_utils.views import APIView, Response
from throttling import AuthRateThrottle

User = get_user_model()


class VerifyAccountView(APIView):
    """API View for handling account verification."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Process a request to resend an account verification email."""

        # Validate required email field
        email = request.data.get("email", None)
        if email is None:
            return self.response(
                {
                    "message": "Please provide a valid email address",
                    "errors": [
                        {
                            "field": "email",
                            "code": "required",
                            "message": "Email address is required",
                            "details": None,
                        }
                    ],
                },
                self.status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.response(
                {
                    "message": "User account not found",
                    "errors": [
                        {
                            "field": "email",
                            "code": "not_exist",
                            "message": "We could not find an account with this email address",
                            "details": None,
                        }
                    ],
                },
                self.status.HTTP_400_BAD_REQUEST,
            )

        if not getattr(user, "is_verified", False):
            # Generate verification token and URL
            generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
            token = generator.generate()
            if token is None:
                return self.response(
                    {
                        "message": "Token generation failed",
                        "errors": [
                            {
                                "field": "token",
                                "code": "generation_failed",
                                "message": "Failed to generate verification token. Please try again later.",
                                "details": None,
                            }
                        ],
                    },
                    self.status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            activate_url = f"{settings.FRONTEND_URL}/auth/verify-user-account/{token}"

            # Send verification email
            SendEmail(
                {
                    "subject": "Account Verification Request",
                    "emails": {"to_emails": [email]},
                    "context": {"user": user, "activate_url": activate_url},
                    "templates": {
                        "txt": "users/verify_account/confirm_message.txt",
                        "html": "users/verify_account/confirm_message.html",
                    },
                }
            )
            return self.response(
                {
                    "message": "Account verification email sent successfully",
                    "data": {
                        "detail": "A verification link has been sent to your email. Please check your inbox."
                    },
                },
                self.status.HTTP_200_OK,
            )
        else:
            return self.response(
                {
                    "message": "Account already verified",
                    "data": {
                        "detail": "This Account has already been verified. You can proceed to sign in."
                    },
                },
                self.status.HTTP_200_OK,
            )
