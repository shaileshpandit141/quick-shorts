# Django imports
from django.utils import timezone
from django.contrib.auth import get_user_model

# Django REST framework imports
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

# Local imports
from permissions import AllowAny
from utils import FieldValidator
from users.serializers import SigninTokenSerializer
from throttling import AnonRateThrottle
from quick_utils.views import QuickAPIView, Response
from quick_utils.format_serializer_errors import format_serializer_errors

User = get_user_model()


class SigninTokenView(TokenObtainPairView, QuickAPIView):
    """Custom JWT token view that handles user authentication using email/username and password."""

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = SigninTokenSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Handle user authentication and return JWT tokens."""

        # Validate required fields
        clean_data = FieldValidator(request.data, ['email', 'password'])  # type: ignore
        if not clean_data.is_valid():
            return self.response({
                "message": "Sign in failed",
                "errors": clean_data.errors,
            }, status.HTTP_400_BAD_REQUEST)

        # Handle username-based login by fetching associated email
        data = clean_data.data.copy()
        if not '@' in clean_data.get('email'):
            try:
                user = User.objects.get(username=clean_data.get('email'))
                data['email'] = user.email
            except User.DoesNotExist:
                return self.response({
                    "message": "Sign in failed",
                    'errors': [{
                        "field": "none",
                        "code": "signin_failed",
                        "message": "Please provide valid authentication credentials.",
                        "details": None
                    }]
                }, status.HTTP_400_BAD_REQUEST)

        # Validate credentials with serializer
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return self.response({
                "message": "Sign in failed",
                'errors': format_serializer_errors(serializer.errors),
            }, status.HTTP_400_BAD_REQUEST)

        # Get the authenticated user from the serializer
        user = serializer.validated_data.get('user')

        # Check email verification status for non-superusers
        if user and not user.is_superuser and not user.is_verified:
            return self.response({
                "message": "Sign in failed - account not verified",
                'errors': [{
                    "field": "none",
                    "code": "signin_failed",
                    "message": "Please verify your account before signing in",
                    "details": None
                }]
            }, status.HTTP_401_UNAUTHORIZED)

        # Update last login timestamp
        if user:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

        # Return successful response with JWT tokens
        return self.response({
            "message": "Welcome back! Sign in successful",
            "data": {
                "access_token": serializer.validated_data["access"],
                "refresh_token": serializer.validated_data["refresh"],
            }
        }, status.HTTP_200_OK)
