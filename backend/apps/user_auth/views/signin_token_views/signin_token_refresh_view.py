from core.views import BaseAPIView, Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class SigninTokenRefreshView(BaseAPIView):
    """Custom token refresh view for handling JWT token refresh operations."""

    def post(self, request, *args, **kwargs) -> Response:
        """Handle token refresh POST requests."""

        refresh_token = request.data.get("refresh_token", None)

        # Validate the refresh_token is empty or not
        if refresh_token is None:
            return self.handle_error(
                "Failed to refresh token - refresh token is missing",
                {"refresh_token": ["Refresh token field cannot be empty"]},
            )

        # Handle Token refresh logic
        try:
            # Create a new refresh token object
            jwt_tokens = RefreshToken(refresh_token)
            return self.handle_success(
                "Access token refreshed successfully",
                {"access_token": str(jwt_tokens.access_token)},
            )
        except (TokenError, InvalidToken) as error:
            return self.handle_error(
                "Token refresh failed - invalid or expired refresh token provided",
                {"refresh_token": [str(error)]},
            )
