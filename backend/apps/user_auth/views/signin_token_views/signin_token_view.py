from django.utils import timezone
from permissions import AllowAny
from core.views import BaseAPIView, Response
from throttling import AuthRateThrottle
from core.get_jwt_tokens_for_user import get_jwt_tokens_for_user
from user_auth.models import User


class SigninTokenView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        data = request.data

        email = data.get("email", None)
        password = data.get("password", None)

        if email is None or password is None:
            errors = []
            # Check if user is password provide or not
            if password is None:
                errors.append(
                    {
                        "field": "password",
                        "code": "blank",
                        "message": "password field can not be blank.",
                        "details": {
                            "password": "add password field in the request payload."
                        },
                    }
                )

            # Append if only email is not provided
            errors.append(
                {
                    "field": "email",
                    "code": "blank",
                    "message": "email field can not be blank.",
                    "details": {"email": "add email field in the request payload."},
                }
            )

            # Return the error response
            return self.handle_error("Sign in request is failed", errors)

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
                    [
                        {
                            "field": "none",
                            "code": "signin_failed",
                            "message": "Please verify your account before signing in.",
                        }
                    ],
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
                "Sign in request is failed",
                [
                    {
                        "field": "none",
                        "code": "signin_failed",
                        "message": str(error),
                    }
                ],
            )
