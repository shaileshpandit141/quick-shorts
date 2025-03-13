from core.views import BaseAPIView, Response
from permissions import AllowAny
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from throttling import AnonRateThrottle


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
                {"refresh_token": ["refresh_token filed can not be blank."]},
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
                {"refresh_token": [str(error)]},
            )
