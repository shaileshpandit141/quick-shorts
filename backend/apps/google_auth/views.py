from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from google.auth.transport import requests
from google.oauth2 import id_token
from requests import get, post

from core.get_jwt_tokens_for_user import get_jwt_tokens_for_user
from core.save_image import save_image
from core.views import BaseAPIView, Response

User = get_user_model()


class GoogleLoginView(BaseAPIView):
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
        return self.handle_success(
            "Google sign in URL generated successfully",
            {
                "login_url": login_url,
            },
        )


class GoogleTokenExchangeView(BaseAPIView):
    def get(self, request) -> Response:
        """Exchange authorization code for an access token."""
        auth_code = request.GET.get("code")

        if not auth_code:
            return self.handle_error(
                "Failed to get access token",
                {"code": ["google generated code is not found."]},
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
            return self.handle_error(
                "Failed to get google access token",
                {"code": ["Google not return access token in reponse."]},
            )

        return self.handle_success(
            "Google Access token retrieved successfully",
            {"token": token_data["access_token"]},
        )


class GoogleCallbackView(BaseAPIView):
    def post(self, request) -> Response:
        """Verify Google token (ID token or access token)."""
        token = request.data.get("token")

        if not token:
            return self.handle_error(
                "Authentication Googel token not provided",
                {"token": ["Please provide a valid authentication token."]},
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
                    return self.handle_error(
                        "The provided authentication token is invalid",
                        {
                            "token": [
                                "The provided authentication token is invalid or expire. Please try again."
                            ]
                        },
                    )

                google_data = response.json()

            # Extract user details
            email = google_data.get("email")
            username = email.split("@")[0]
            profile_picture = google_data.get("picture")

            if not email:
                return self.handle_error(
                    "The provided authentication token is invalid",
                    {
                        "token": [
                            "The provided authentication token is invalid or expire. Please try again."
                        ]
                    },
                )

            # Handle user profile picture
            picture = save_image(User, "picture", profile_picture, username)

            # Save user and generate JWT tokens
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": google_data.get("given_name"),
                    "last_name": google_data.get("family_name"),
                    "username": username,
                    "picture": picture,
                    "is_verified": True,
                },
            )

            # Update user details if they already exist
            user.first_name = google_data.get("given_name")
            user.last_name = google_data.get("family_name")
            setattr(user, "picture", picture)
            setattr(user, "is_verified", True)
            user.save()

            tokens = get_jwt_tokens_for_user(user)

            return self.handle_success(
                "Google Sign in successful",
                {**tokens},
            )

        except Exception as error:
            return self.handle_error(
                "An error occurred during google authentication", {"detail": str(error)}
            )
