from typing import cast

from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from rest_framework_simplejwt.tokens import RefreshToken


def get_jwt_tokens_for_user(user: Model) -> dict[str, str]:
    refresh = RefreshToken.for_user(cast(AbstractUser, user))
    return {
        "refresh_token": str(refresh),
        "access_token": str(getattr(refresh, "access_token")),
    }
