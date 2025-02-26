from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from requests import post, get

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


class GoogleTokenExchangeView(APIView):
    def get(self, request) -> Response:
        """Step 2: Exchange authorization code for an access token."""
        auth_code = request.GET.get("code")

        if not auth_code:
            return self.response(
                {
                    "message": "Failed to get access token",
                    "errors": [
                        {
                            "field": "code",
                            "code": "invalid",
                            "message": "code is not found",
                            "details": None,
                        }
                    ],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        }

        # Send request to Google to exchange code for a token
        response = post(token_url, data=data)
        token_data = response.json()

        if "access_token" not in token_data:
            return self.response(
                {
                    "message": "Failed to get access token",
                    "errors": [
                        {
                            "field": "token",
                            "code": "invalid",
                            "message": token_data,
                            "details": None,
                        }
                    ],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self.response(
            {
                "message": "Access token retrieved successfully",
                "data": {"token": token_data["access_token"]},
            },
            status=status.HTTP_200_OK,
        )


class GoogleCallbackView(APIView):
    def post(self, request) -> Response:
        """Verify Google token (ID token or access token)."""
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
            google_data = None

            # Try to verify as an ID Token first
            try:
                google_data = id_token.verify_oauth2_token(
                    token, requests.Request(), settings.GOOGLE_CLIENT_ID
                )
            except ValueError:
                # If that fails, treat it as an OAuth access token and fetch user info
                google_user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
                headers = {"Authorization": f"Bearer {token}"}
                response = get(google_user_info_url, headers=headers)

                if response.status_code != 200:
                    return self.response(
                        {
                            "message": "Invalid token",
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

                google_data = response.json()

            # Extract user details
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

            # Handle user profile picture
            avatar = save_image(User, "avatar", profile_picture, username)

            # Save user and generate JWT tokens
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": google_data.get("given_name"),
                    "last_name": google_data.get("family_name"),
                    "username": username,
                    "avatar": avatar,
                    "is_verified": True,
                },
            )

            # Update user details if they already exist
            user.first_name = google_data.get("given_name")
            user.last_name = google_data.get("family_name")
            setattr(user, "avatar", avatar)
            setattr(user, "is_verified", True)
            user.save()

            tokens = get_jwt_tokens_for_user(user)

            return self.response(
                {
                    "message": "Sign in successful",
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
