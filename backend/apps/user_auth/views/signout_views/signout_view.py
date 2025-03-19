from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from core.views import BaseAPIView, Response
from permissions import AllowAny
from throttling import AnonRateThrottle


class SignoutView(BaseAPIView):
    """API view for user sign out functionality."""

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle user sign out by blacklisting their refresh token."""

        refresh_token = request.data.get("refresh_token", "")

        try:
            # Get and blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return self.handle_success(
                "You have been successfully signed out.",
                {"detail": "Your session has been terminated."},
            )
        except TokenError:
            return self.handle_error(
                "Unable to process refresh token.",
                {"detail": "The provided token is invalid or has already expired."},
            )
