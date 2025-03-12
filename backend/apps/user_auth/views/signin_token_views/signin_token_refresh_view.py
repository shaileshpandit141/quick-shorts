from typing import NoReturn

from permissions import AllowAny
from core.views import BaseAPIResponseHandler, Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenRefreshView
from throttling import AnonRateThrottle


class SigninTokenRefreshView(TokenRefreshView, BaseAPIResponseHandler):
    """Custom token refresh view for handling JWT token refresh operations."""

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get_serializer(self, *args, **kwargs) -> NoReturn:
        """Customize serializer to handle refresh token field name."""

        data = self.request.data.copy()  # type: ignore
        refresh_token = data.pop("refresh_token", None)
        if refresh_token and isinstance(refresh_token, list):
            if len(refresh_token) > 0:
                refresh_token = refresh_token[0]
        if not refresh_token:
            raise serializers.ValidationError(
                {"refresh_token": "This field is required."}
            )

        data["refresh"] = refresh_token
        return super().get_serializer(data=data)

    def post(self, request, *args, **kwargs) -> Response:
        """Handle token refresh POST requests."""

        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return self.success(
                    {
                        "message": "Token refreshed successfully",
                        "data": {
                            "access_token": getattr(request, "data", {}).get(
                                "access", None
                            ),
                        },
                    }
                )

            # Invalid or expired refresh token
            raise ValidationError("Invalid or expired refresh token.")
        except ValidationError as error:
            return self.error(
                {
                    "message": "Oops! something went wrong. Please try again later",
                    "errors": [
                        {
                            "field": "none",
                            "code": "refresh_token",
                            "message": str(error),
                        }
                    ],
                }
            )
