from django.contrib.auth import get_user_model
from permissions import AllowAny
from limited_time_token_handler import LimitedTimeTokenDecoder, TokenError
from quick_utils.views import APIView, Response
from throttling import AuthRateThrottle

User = get_user_model()


class VerifyAccountConfirmView(APIView):
    """API View for verifying user accounts via email confirmation."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle POST request for email verification"""

        # Validate required fields
        token = request.data.get("token", None)
        if token is None:
            return self.response(
                {
                    "message": "Token is required",
                    "errors": [
                        {
                            "field": "token",
                            "code": "token_required",
                            "message": "Token is required",
                            "details": None,
                        }
                    ],
                },
                self.status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Decode verification token
            decoder = LimitedTimeTokenDecoder(token)
            if not decoder.is_valid():
                raise TokenError("Invalid token")

            data = decoder.decode()
            user = User.objects.get(id=data.get("user_id"))

            # Check if already verified
            if getattr(user, "is_verified", False):
                return self.response(
                    {
                        "message": "Account already verified",
                        "data": {"detail": "Account already verified."},
                    },
                    self.status.HTTP_200_OK,
                )

            # Update verification status
            setattr(user, "is_verified", True)
            user.save()
            return self.response(
                {
                    "message": "Account verified successfully",
                    "data": {"detail": "Account verified successfully"},
                },
                self.status.HTTP_200_OK,
            )

        except (ValueError, TokenError) as error:
            return self.response(
                {
                    "message": "Invalid or expired token",
                    "errors": [
                        {
                            "field": "token",
                            "code": "invalid",
                            "message": str(error),
                            "details": None,
                        }
                    ],
                },
                self.status.HTTP_400_BAD_REQUEST,
            )
