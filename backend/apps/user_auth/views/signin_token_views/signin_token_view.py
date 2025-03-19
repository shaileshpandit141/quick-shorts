from django.utils import timezone
from user_auth.models import User

from core.get_jwt_tokens_for_user import get_jwt_tokens_for_user
from core.views import BaseAPIView, Response
from permissions import AllowAny
from throttling import AuthRateThrottle


class SigninTokenView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        data = request.data

        email = data.get("email", None)
        password = data.get("password", None)

        # Handle if user not include email in payload
        if email is None:
            return self.handle_error(
                "Sign in request is failed",
                {"email": ["Email field can not be blank."]},
            )

        # Handle if user not include password in payload
        if password is None:
            return self.handle_error(
                "Sign in request is failed",
                {"password": ["Password field can not be blank."]},
            )

        # Handle email and username based signin
        try:
            user = None
            if "@" in email:
                user = self.get_object(User, email=email)
            else:
                user = self.get_object(User, username=email)

            # Check is user is None
            if user is None:
                raise Exception("Something is not correct. try again later!")

            # Check user password is currect or not
            if not user.check_password(password):
                raise Exception("Please provide valid authentication credentials.")

            # Handle success signin response
            if not user.is_superuser and not user.is_verified:
                return self.handle_error(
                    "Sign in request is failed - account not verified",
                    {"detail": "Please verify your account before signing in."},
                )

            # Generate jwt toke for requested user
            jwt_tokens = get_jwt_tokens_for_user(user)

            # Update last login timestamp
            if user:
                user.last_login = timezone.now()
                user.save(update_fields=["last_login"])

            # Return success response
            return self.handle_success(
                "Welcome back! Sign in request is successful", jwt_tokens
            )
        except Exception as error:
            return self.handle_error(
                "Sign in request is failed", {"detail": str(error)}
            )
