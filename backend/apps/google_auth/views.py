from email import message
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status

from quick_utils.get_jwt_tokens_for_user import get_jwt_tokens_for_user
from quick_utils.save_image import save_image
from quick_utils.views import APIView, Response

User = get_user_model()


class GoogleLoginView(APIView):
    def get(self, request) -> Response:
        google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
        }
        login_url = f"{google_auth_url}?{urlencode(params)}"
        return self.response(
            {
                "message": "Google sign in URL generated successfully",
                "data": {"login_url": login_url},
            },
            status=status.HTTP_200_OK,
        )


class GoogleCallbackView(APIView):
    def post(self, request) -> Response:
        token = request.data.get("token")
        if not token:
            return self.response(
                {
                    "message": "Authentication token not provided",
                    "errors": [
                        {
                            "field": "none",
                            "code": "token_not_provided",
                            "message": "Please provide a valid authentication token.",
                            "details": None,
                        },
                    ],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Verify token with Google
            google_data = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )
            email = google_data.get("email")
            username = email.split("@")[0]
            profile_picture = google_data.get("picture")

            if not email:
                return self.response(
                    {
                        "message": "Invalid authentication token",
                        "errors": [
                            {
                                "field": "none",
                                "code": "invalid_token",
                                "message": "The provided authentication token is invalid. Please try again.",
                                "details": None,
                            },
                        ],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            avatar = save_image(User, "avatar", profile_picture, username)

            # Create or update user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": google_data.get("given_name"),
                    "last_name": google_data.get("family_name"),
                    "username": email.split("@")[0],
                    "avatar": avatar,
                    "is_verified": True,
                },
            )

            message = "Sign in successful"
            if not created:
                # Override the message if use is already exist
                message = "Welcome back! Sign in successful"

                # Update user details if they already exist
                user.first_name = google_data.get("given_name")
                user.last_name = google_data.get("family_name")
                setattr(user, "avatar", avatar)
                setattr(user, "is_verified", True)
                user.save()

            # Generate JWT tokens
            tokens = get_jwt_tokens_for_user(user)

            return self.response(
                {
                    "message": message,
                    "data": {**tokens},
                },
                status=status.HTTP_200_OK,
            )

        except Exception as error:
            return self.response(
                {
                    "message": "An error occurred during authentication",
                    "errors": [
                        {
                            "field": "none",
                            "code": "invalid_token",
                            "message": str(error),
                            "details": None,
                        },
                    ],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
