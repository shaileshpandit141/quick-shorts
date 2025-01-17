# Types imports
from typing import NoReturn

# Django REST framework imports
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenRefreshView

# Local imports
from quick_utils.views import QuickAPIView, Response
from permissions import AllowAny
from throttling import AnonRateThrottle


class SigninTokenRefreshView(TokenRefreshView, QuickAPIView):
    """Custom token refresh view for handling JWT token refresh operations."""

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get_serializer(self, *args, **kwargs) -> NoReturn:
        """Customize serializer to handle refresh token field name."""

        data = self.request.data.copy()  # type: ignore
        refresh_token = data.pop('refresh_token', None)
        if refresh_token and isinstance(refresh_token, list):
            if len(refresh_token) > 0:
                refresh_token = refresh_token[0]

        if not refresh_token:
            raise serializers.ValidationError({
                'refresh_token': 'This field is required.'
            })

        data['refresh'] = refresh_token
        return super().get_serializer(data=data)

    def post(self, request, *args, **kwargs) -> Response:
        """Handle token refresh POST requests."""

        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return self.response({
                    "message": "Token refreshed successfully",
                    "data": {
                        "access_token": response.data.get("access", None)  # type: ignore
                    }
                }, status.HTTP_200_OK)

            # Invalid or expired refresh token
            return self.response({
                'message': 'Failed to refresh token',
                'errors': [{
                    "field": "refresh_token",
                    "code": "invalid_refresh_token",
                    "message": "Invalid or expired refresh token",
                    "details": None
                }]
            }, status.HTTP_400_BAD_REQUEST)

        except ValidationError as error:
            # Handle case where no refresh token is provided
            if 'refresh_token' in str(error):
                return self.response({
                    'message': 'Refresh token is required',
                    'errors': [{
                        "field": "refresh_token",
                        "code": "invalid_refresh_token",
                        "message": "This field is required.",
                        "details": None
                    }]
                }, status.HTTP_400_BAD_REQUEST)

            # Catch other validation errors
            return self.response({
                'message': 'Invalid refresh token provided',
                'errors': [{
                    "field": "refresh_token",
                    "code": "invalid_refresh_token",
                    "message": "The refresh token provided is invalid or expired.",
                    "details": None
                }]
            }, status.HTTP_400_BAD_REQUEST)
