from permissions import AllowAny
from core.views import BaseAPIView, Response
from throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class SigninTokenRefreshView(BaseAPIView):
    """Custom token refresh view for handling JWT token refresh operations."""

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle token refresh POST requests."""

        refresh_token = request.data.get("refresh_token", None)

        # Validate the refresh_token is empty or not
        if refresh_token is None:
            return self.handle_error(
                "Token refresh request was failed",
                [
                    {
                        "field": "refresh_token",
                        "code": "blank",
                        "message": "refresh_token filed can not be blank.",
                        "details": {
                            "refresh_token": "add refresh_token field in the request payload."
                        },
                    }
                ],
            )

        # Handle Token refresh logic
        try:
            # Create a new refresh token object
            jwt_tokens = RefreshToken(refresh_token)
            return self.handle_success(
                "Token refreshed successfully",
                {"access_token": str(jwt_tokens.access_token)},
            )
        except (TokenError, InvalidToken) as error:
            return self.handle_error(
                "Invalid or expired refresh token",
                [
                    {
                        "field": "none",
                        "code": "refresh_token",
                        "message": str(error),
                    }
                ],
            )
