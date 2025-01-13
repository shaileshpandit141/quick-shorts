# Django imports
from django.contrib.auth import get_user_model

# Local imports
from quick_utils.views import QuickAPIView, Response
from permissions import IsAuthenticated, IsVerified
from throttling import UserRateThrottle
from utils import FieldValidator
from users.serializers import UserSerializer

User = get_user_model()


class UserInfoAPIView(QuickAPIView):
    """API View for managing authenticated user information."""

    permission_classes = [IsAuthenticated, IsVerified]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs) -> Response:
        """Retrieve current user"s profile information."""

        user = request.user
        serializer = UserSerializer(instance=user, many=False)
        return self.success_response({
            "message": "Profile information retrieved successfully",
            "data": serializer.data
        }, self.status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs) -> Response:
        """Update authenticated user's profile information."""

        user = request.user
        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name")
        }

        # Validate required fields
        clean_data = FieldValidator(data, ["first_name", "last_name"])
        if not clean_data.is_valid():
            return self.error_response({
                "message": "Required fields are missing or invalid",
                "errors": clean_data.errors
            }, self.status.HTTP_400_BAD_REQUEST)

        # Update user instance with new data
        serializer = UserSerializer(
            data=data,
            instance=user,
            many=False,
            partial=True
        )

        if not serializer.is_valid():
            return self.error_response({
                "message": "Invalid request data",
                "errors": self.format_serializer_errors(
                    serializer.errors
                )
            }, self.status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return self.success_response({
            "message": "Profile information updated successfully",
            "data": serializer.data
        }, self.status.HTTP_200_OK)
