from permissions import AllowAny
from quick_utils.views import APIView, Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from throttling import AuthRateThrottle
from utils import FieldValidator


class SignoutView(APIView):
    """API view for user sign out functionality."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle user sign out by blacklisting their refresh token."""

        # Validate the refresh token is present in request data
        clean_data = FieldValidator(request.data, ["refresh_token"])
        if not clean_data.is_valid():
            return self.response(
                {
                    "message": "Please provide a valid refresh token",
                    "errors": clean_data.errors,
                },
                self.status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Get and blacklist the refresh token
            token = RefreshToken(clean_data.get("refresh_token"))
            token.blacklist()

            return self.response(
                {
                    "message": "You have been successfully signed out",
                    "data": {"detail": "Your session has been terminated"},
                },
                self.status.HTTP_200_OK,
            )

        except TokenError:
            return self.response(
                {
                    "message": "Unable to process token",
                    "errors": [
                        {
                            "field": "none",
                            "code": "invalid_token",
                            "message": "The provided token is invalid or has already expired",
                            "details": None,
                        }
                    ],
                },
                self.status.HTTP_400_BAD_REQUEST,
            )
