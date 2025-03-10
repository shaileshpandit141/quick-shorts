from typing import TypedDict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class JWTPayload(TypedDict):
    refresh_token: str
    access_token: str


def get_jwt_tokens_for_user(user: AbstractUser) -> JWTPayload:
    refresh = RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(getattr(refresh, "access_token")),
    }
