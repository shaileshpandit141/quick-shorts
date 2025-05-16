from django.contrib.auth import get_user_model
from user_auth.serializers import UserSerializer

from apps.user_auth.mixins import IsUserAccountVerifiedPermissionsMixin
from core.views import BaseAPIView, Response

User = get_user_model()


class UserInfoView(IsUserAccountVerifiedPermissionsMixin, BaseAPIView):
    """API View for managing authenticated user information."""

    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs) -> Response:
        """Retrieve current user"s profile information."""

        user = request.user
        serializer = self.get_serializer(instance=user, many=False)
        return self.handle_success(
            "User profile data fetched successfully",
            serializer.data,
        )

    def patch(self, request, *args, **kwargs) -> Response:
        """Update authenticated user's profile information."""

        # Create user serializer instance with new data
        serializer = self.get_serializer(
            data=request.data,
            instance=request.user,
            many=False,
            partial=True,
        )

        if not serializer.is_valid():
            return self.handle_error(
                "Unable to update profile - invalid data provided",
                serializer.errors,
            )

        serializer.save()
        return self.handle_success(
            "User profile has been updated successfully",
            serializer.data,
        )
