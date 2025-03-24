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
                "Sign in failed - Email required",
                {"email": ["Please enter your email address"]},
            )

        # Handle if user not include password in payload
        if password is None:
            return self.handle_error(
                "Sign in failed - Password required",
                {"password": ["Please enter your password"]},
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
                raise Exception(
                    "Invalid credentials. Please check your email/username and try again."
                )

            # Check user password is currect or not
            if not user.check_password(password):
                raise Exception("Invalid password. Please try again.")

            # Handle success signin response
            if not user.is_superuser and not user.is_verified:
                return self.handle_error(
                    "Sign in failed - Email verification required",
                    {
                        "detail": "Please verify your email address to sign in. Check your inbox for the verification link."
                    },
                )

            # Generate jwt toke for requested user
            jwt_tokens = get_jwt_tokens_for_user(user)

            # Update last login timestamp
            if user:
                setattr(user, "last_login", timezone.now())
                user.save(update_fields=["last_login"])

            # Return success response
            return self.handle_success(
                "Welcome back! You have successfully signed in", jwt_tokens
            )
        except Exception as error:
            return self.handle_error("Sign in failed", {"detail": str(error)})
