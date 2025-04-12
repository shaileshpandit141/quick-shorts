from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from .permissions import IsUserAccountVerified
from .throttles import AuthUserRateThrottle


class IsUserAuthenticatedPermissionsMixin:
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class IsUserAccountVerifiedPermissionsMixin:
    permission_classes = [IsAuthenticated, IsUserAccountVerified]
    throttle_classes = [UserRateThrottle]


class AuthUserRateThrottleMinin:
    permission_classes = [AllowAny]
    throttle_classes = [AuthUserRateThrottle]
