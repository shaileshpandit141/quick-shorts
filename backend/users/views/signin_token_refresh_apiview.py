# Django REST framework imports
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenRefreshView

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import Response


class SigninTokenRefreshAPIView(TokenRefreshView):
    """
    Custom token refresh view for updating JWT tokens.
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get_serializer(self, *args, **kwargs) -> TokenRefreshView:
        """
        Customize serializer to handle refresh token field name.
        """
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

    def get(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('get')

    def post(self, request, *args, **kwargs) -> Response.type:
        """
        Handle token refresh requests.
        """
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response.success({
                    'message': 'Access token successfully renewed',
                    'data': {
                        'access_token': response.data.get('access', None)  # type: ignore
                    }
                }, status.HTTP_200_OK)

            # Invalid or expired refresh token
            return Response.error({
                'message': 'Unable to refresh access token',
                'errors': {
                    'non_field_errors': [
                        'Invalid or expired refresh token'
                    ]
                }
            }, status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            print(f'Validation Error: {e}')
            # Handle case where no refresh token is provided
            if 'refresh_token' in str(e):
                return Response.error({
                    'message': 'Missing required refresh token',
                    'errors': {
                        'refresh_token': [
                            'This field is required.'
                        ]
                    }
                }, status.HTTP_400_BAD_REQUEST)

            # Catch other validation errors
            return Response.error({
                'message': 'Invalid refresh token',
                'errors': {
                    'refresh_token': [
                        'The refresh token provided is invalid or expired.'
                    ]
                }
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('put')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('patch')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('delete')

    def options(self, request, *args, **kwargs) -> Response.type:
        return Response.options(['POST'])
