from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from .permissions import IsUserAccountVerified
from .throttles import AuthUserRateThrottle


class IsUserAuthenticatedPermissionsMixin:
    permissions_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class IsUserAccountVerifiedPermissionsMixin:
    permissions_classes = [IsAuthenticated, IsUserAccountVerified]
    throttle_classes = [UserRateThrottle]


class AuthUserRateThrottleMinin:
    throttle_classes = [AllowAny]
    throttle_classes = [AuthUserRateThrottle]
