# Django imports
from django.utils import timezone
from django.contrib.auth import get_user_model

# Django REST framework imports
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import Response, FieldValidator
from users.serializers import SigninTokenSerializer

User = get_user_model()


class SigninTokenAPIView(TokenObtainPairView):
    """
    Custom JWT token view that handles user authentication using email/username and password.

    Attributes:
        permission_classes: List of permission classes, allows any user (authenticated or not)
        throttle_classes: List of throttle classes to limit request rates
        serializer_class: Serializer class for processing signin data
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = SigninTokenSerializer

    def get(self, request, *args, **kwargs) -> Response.type:
        """Disallow GET method"""
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs):
        """
        Handle user authentication and return JWT tokens.

        Args:
            request: HTTP request object containing user credentials
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            Response object containing:
                - On success: JWT access and refresh tokens
                - On failure: Error message with details

        Raises:
            HTTP 400: For invalid credentials or validation errors
            HTTP 401: For unverified user accounts
        """
        # Validate required fields
        clean_data = FieldValidator(request.data, ['email', 'password'])  # type: ignore
        if not clean_data.is_valid():
            return Response.error({
                'message': 'Sign in failed',
                'errors': clean_data.get_errors()
            }, status.HTTP_400_BAD_REQUEST)

        # Handle username-based login by fetching associated email
        data = clean_data.data.copy()
        if not '@' in clean_data.get('email'):
            try:
                user = User.objects.get(username=clean_data.get('email'))
                data['email'] = user.email
            except User.DoesNotExist:
                return Response.error({
                    'message': 'Sign in failed',
                    'errors': {
                        'non_field_errors': [
                            'Please provide valid authentication credentials.'
                        ]
                    }
                }, status.HTTP_400_BAD_REQUEST)

        # Validate credentials with serializer
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response.error({
                'message': 'Sign in failed',
                'errors': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        # Get the authenticated user from the serializer
        user = serializer.validated_data.get('user')

        # Check email verification status for non-superusers
        if user and not user.is_superuser and not user.is_verified:
            return Response.error({
                'message': 'Sign in failed - account not verified',
                'errors': {
                    'non_field_errors': [
                        'Please verify your account before signing in'
                    ]
                }
            }, status.HTTP_401_UNAUTHORIZED)

        # Update last login timestamp
        if user:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

        # Return successful response with JWT tokens
        return Response.success({
            'message': 'Welcome back! Sign in successful',
            'data': {
                'access_token': serializer.validated_data['access'],
                'refresh_token': serializer.validated_data['refresh'],
            }
        }, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs) -> Response.type:
        """Disallow PUT method"""
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """Disallow PATCH method"""
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        """Disallow DELETE method"""
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """Return allowed HTTP methods for this endpoint."""
        return Response.options(['POST'])
