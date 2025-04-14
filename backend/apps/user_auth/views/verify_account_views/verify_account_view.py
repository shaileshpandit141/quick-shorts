from apps.user_auth.mixins import AuthUserRateThrottleMinin
from core.send_email import SendEmail
from core.views import BaseAPIView, Response
from django.contrib.auth import get_user_model
from limited_time_token_handler import LimitedTimeTokenGenerator

User = get_user_model()


class VerifyAccountView(AuthUserRateThrottleMinin, BaseAPIView):
    """API View for handling account verification."""

    def post(self, request, *args, **kwargs) -> Response:
        """Process a request to resend an account verification email."""

        # Gatting submitted data from request
        email = request.data.get("email", None)
        active_url = request.data.get("active_url", None)

        # Handle if user not include email in payload
        if email is None:
            return self.handle_error(
                "Email is required",
                {"email": ["Please provide an email address."]},
            )

        user = self.get_object(User, email=email)
        if user is None:
            return self.handle_error(
                "Account not found",
                {
                    "email": [
                        "No account exists with this email address. Please sign up first."
                    ]
                },
            )

        if not getattr(user, "is_verified", False):
            # Generate verification token and URL
            generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
            token = generator.generate()
            if token is None:
                return self.handle_error(
                    "Verification token generation failed",
                    {
                        "detail": "Unable to generate verification token. Please try again in a few minutes."
                    },
                )

            # Send verification email
            SendEmail(
                {
                    "subject": "Account Verification Request",
                    "emails": {"to_emails": [email]},
                    "context": {"user": user, "activate_url": f"{active_url}/{token}"},
                    "templates": {
                        "txt": "users/verify_account/confirm_message.txt",
                        "html": "users/verify_account/confirm_message.html",
                    },
                }
            )
            return self.handle_success(
                "Verification email sent",
                {
                    "detail": "We've sent a verification link to your email address. Please check your inbox and spam folder."
                },
            )
        else:
            return self.handle_success(
                "Account Already Verified",
                {
                    "detail": "Your account has already been verified. Please proceed to sign in with your credentials."
                },
            )
