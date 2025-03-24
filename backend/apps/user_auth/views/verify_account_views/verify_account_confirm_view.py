from django.contrib.auth import get_user_model
from limited_time_token_handler import LimitedTimeTokenDecoder, TokenError

from core.views import BaseAPIView, Response
from permissions import AllowAny
from throttling import AuthRateThrottle

User = get_user_model()


class VerifyAccountConfirmView(BaseAPIView):
    """API View for verifying user accounts via email confirmation."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle POST request for email verification"""

        # Validate required fields
        token = request.data.get("token", None)

        # Validate the blank token
        if token is None:
            return self.handle_error(
                "Token is missing",
                {
                    "token": [
                        "Token field is required. Please provide a valid verification token."
                    ]
                },
            )

        try:
            # Decode verification token
            decoder = LimitedTimeTokenDecoder(token)
            if not decoder.is_valid():
                raise TokenError("The verification token is invalid or has expired.")

            data = decoder.decode()
            user = User.objects.get(id=data.get("user_id"))

            # Check if already verified
            if getattr(user, "is_verified", False):
                return self.handle_success(
                    "Account Already Verified",
                    {
                        "detail": "This account has already been verified. No further action is needed."
                    },
                )

            # Update verification status
            setattr(user, "is_verified", True)
            user.save()
            return self.handle_success(
                "Account verification successful",
                {"detail": "Your account has been verified successfully."},
            )

        except (ValueError, TokenError):
            return self.handle_error(
                "Invalid verification token",
                {
                    "detail": "The provided verification token is invalid or has expired."
                },
            )
