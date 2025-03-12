from django.contrib.auth import get_user_model
from permissions import IsVerified
from core.views import BaseAPIView, Response
from throttling import UserRateThrottle
from user_auth.serializers import UserSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class UserInfoView(BaseAPIView):
    """API View for managing authenticated user information."""

    permission_classes = [IsAuthenticated, IsVerified]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs) -> Response:
        """Retrieve current user"s profile information."""

        user = request.user
        serializer = UserSerializer(instance=user, many=False)
        return self.handle_success(
            "Profile information retrieved successfully.",
            serializer.data,
        )

    def patch(self, request, *args, **kwargs) -> Response:
        """Update authenticated user's profile information."""

        # Create user serializer instance with new data
        serializer = UserUpdateSerializer(
            data=request.data,
            instance=request.user,
            many=False,
            partial=True,
        )

        if not serializer.is_valid():
            return self.handle_error(
                "Invalid to procode request with provided data.",
                self.formatter.format(serializer.errors),
            )

        serializer.save()
        return self.handle_success(
            "Profile information updated successfully.",
            serializer.data,
        )
