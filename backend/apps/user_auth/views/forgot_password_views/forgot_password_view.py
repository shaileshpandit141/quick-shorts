from django.conf import settings
from django.contrib.auth import get_user_model
from limited_time_token_handler import LimitedTimeTokenGenerator

from core.send_email import SendEmail
from core.views import BaseAPIView, Response
from apps.user_auth.mixins import AuthUserRateThrottleMinin

User = get_user_model()


class ForgotPasswordView(AuthUserRateThrottleMinin, BaseAPIView):
    """API endpoint for handling forgot password functionality."""

    def post(self, request, *args, **kwargs) -> Response:
        """Process forgot password request and send reset email."""

        email = request.data.get("emial", "")

        try:
            # Check if user exists with this email or not
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.handle_error(
                "Account is not found with the given credentials.",
                {"email": ["No account exists with this email address."]},
            )

        # Process request for verified users
        if getattr(user, "is_verified", False):
            # Generate reset token
            generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
            token = generator.generate()
            if token is None:
                return self.handle_error(
                    "Failed to generate token. Please try again later.",
                    {"detail": "Failed to generate token. Please try again later."},
                )

            active_url = f"{settings.FRONTEND_URL}/auth/forgot-password-confirm/{token}"
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
            return self.handle_success(
                "Forgot password email sent.",
                {"detail": "Please check your inbox for the Forgot password."},
            )
        else:
            return self.handle_error(
                "Please verify your account to continue.",
                {
                    "detail": "You must verify your account to access this resource.",
                    "code": "account_not_varified",
                },
            )
