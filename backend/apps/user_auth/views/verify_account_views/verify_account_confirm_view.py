from core.views import BaseAPIView, Response
from django.contrib.auth import get_user_model
from limited_time_token_handler import LimitedTimeTokenDecoder, TokenError
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
                "Token can not be blank",
                {
                    "token": [
                        "Token filed is require. Please include it in request payload"
                    ]
                },
            )

        try:
            # Decode verification token
            decoder = LimitedTimeTokenDecoder(token)
            if not decoder.is_valid():
                raise TokenError("Verification token is not valid.")

            data = decoder.decode()
            user = User.objects.get(id=data.get("user_id"))

            # Check if already verified
            if getattr(user, "is_verified", False):
                return self.handle_success(
                    "Your account already verified.",
                    {"detail": "Your account already verified."},
                )

            # Update verification status
            setattr(user, "is_verified", True)
            user.save()
            return self.handle_success(
                "Account verified successfully.",
                {"detail": "Your account verified successfully."},
            )

        except (ValueError, TokenError) as error:
            return self.handle_error(
                "Provided token is Invalid or expired.",
                {"detail": str(error)},
            )
