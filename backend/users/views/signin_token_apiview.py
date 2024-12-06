# Django imports
from django.utils import timezone

# Django REST framework imports
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import Response
from users.serializers import SigninTokenSerializer


class SigninTokenAPIView(TokenObtainPairView):
    """
    Custom JWT token view for user authentication using email and password.
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = SigninTokenSerializer  # Use the custom serializer

    def get(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('get')

    def post(self, request, *args, **kwargs):
        """
        Handle login request and return JWT tokens.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response.error({
                'message': 'Sign in failed',
                'errors': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        # Get the user from the serializer
        user = serializer.validated_data.get('user')

        # Enforce email verification for non-superusers
        if user and not user.is_superuser and not user.is_email_verified:
            return Response.error({
                'message': 'Sign in failed - email not verified',
                'errors': {
                    'non_field_errors': [
                        'Please verify your email address before signing in'
                    ]
                }
            }, status.HTTP_401_UNAUTHORIZED)

        # Update last login timestamp
        if user:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

        # Return tokens from the serializer
        return Response.success({
            'message': 'Welcome back! Sign in successful',
            'data': {
                'access_token': serializer.validated_data['access'],
                'refresh_token': serializer.validated_data['refresh'],
            }
        }, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('put')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('patch')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('delete')

    def options(self, request, *args, **kwargs) -> Response.type:
        return Response.options(['POST'])
