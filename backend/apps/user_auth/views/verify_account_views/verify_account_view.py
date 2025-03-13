from django.conf import settings
from django.contrib.auth import get_user_model
from limited_time_token_handler import LimitedTimeTokenGenerator
from permissions import AllowAny
from core.send_email import SendEmail
from core.views import BaseAPIView, Response
from throttling import AuthRateThrottle

User = get_user_model()


class VerifyAccountView(BaseAPIView):
    """API View for handling account verification."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Process a request to resend an account verification email."""

        # Get email from request
        email = request.data.get("email", None)

        # Handle if user not include email in payload
        if email is None:
            return self.handle_error(
                "Sign up request is failed",
                {"email": ["Email field can not be blank."]},
            )

        user = self.get_object(User, email=email)
        if user is None:
            return self.handle_error(
                "User account not found.",
                {"email": ["We could not find an account with this email address."]},
            )

        if not getattr(user, "is_verified", False):
            # Generate verification token and URL
            generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
            token = generator.generate()
            if token is None:
                return self.handle_error(
                    "Failed to generate an account verification token.",
                    {
                        "detail": "Failed to generate an account verification token. Please try again later."
                    },
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
            return self.handle_success(
                "Account verification email sent successfully.",
                {
                    "detail": "A verification link has been sent to your email. Please check your inbox."
                },
            )
        else:
            return self.handle_success(
                "Account already verified",
                {
                    "detail": "This Account has already been verified. You can proceed to sign in."
                },
            )
