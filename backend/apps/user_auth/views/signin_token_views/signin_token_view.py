from django.contrib.auth import get_user_model
from django.utils import timezone
from permissions import AllowAny
from core.views import BaseAPIResponseHandler, Response
from rest_framework_simplejwt.views import TokenObtainPairView
from throttling import AuthRateThrottle
from user_auth.serializers import SigninTokenSerializer

User = get_user_model()


class SigninTokenView(TokenObtainPairView, BaseAPIResponseHandler):
    """Custom JWT token view that handles user authentication using email/username and password."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]
    serializer_class = SigninTokenSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Handle user authentication and return JWT tokens."""

        email = request.data.get("email", "")  # type: ignore
        password = request.data.get("password", "")  # type: ignore

        # Handle username-based login by fetching associated email
        user_data = {"email": email, "password": password}
        if "@" not in email:
            try:
                user = User.objects.get(username=email)
                user_data["email"] = user.email
            except User.DoesNotExist as error:
                return self.error(
                    {
                        "message": "Sign in request is failed.",
                        "errors": [
                            {
                                "field": "none",
                                "code": "signin_failed",
                                "message": "Please provide valid authentication credentials.",
                                "details": {"detail": str(error)},
                            }
                        ],
                    }
                )

        # Validate credentials with serializer
        serializer = self.get_serializer(data=user_data)
        if not serializer.is_valid():
            return self.error(
                {
                    "message": "Sign in request is failed",
                    "errors": self.formatter(serializer.errors),
                }
            )

        # Get the authenticated user from the serializer
        user = serializer.validated_data.get("user")
        # Check email verification status for non-superusers
        if user and not user.is_superuser and not user.is_verified:
            return self.error(
                {
                    "message": "Sign in request is failed - account not verified",
                    "errors": [
                        {
                            "field": "none",
                            "code": "signin_failed",
                            "message": "Please verify your account before signing in.",
                        }
                    ],
                },
                self.status.HTTP_401_UNAUTHORIZED,
            )

        # Update last login timestamp
        if user:
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])

        # Return successful response with JWT tokens
        return self.success(
            {
                "message": "Welcome back! Sign in request is successful",
                "data": {
                    "access_token": serializer.validated_data["access"],
                    "refresh_token": serializer.validated_data["refresh"],
                },
            }
        )
