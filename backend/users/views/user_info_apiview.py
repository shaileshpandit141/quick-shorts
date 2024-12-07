# Django imports
from django.contrib.auth import get_user_model

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# Local imports
from permissions import IsAuthenticated, IsEmailVerified
from throttles import UserRateThrottle
from utils import Response
from users.serializers import UserSerializer

User = get_user_model()


class UserInfoAPIView(APIView):
    """
    View for retrieving authenticated user information.

    Provides endpoint to get current user's profile data.
    Requires authentication to access.

    Methods:
        get: Retrieve user information

    Attributes:
        permission_classes: Require authentication
        throttle_classes: Rate limiting for authenticated users only
    """
    permission_classes = [IsAuthenticated, IsEmailVerified]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """
        Retrieve current user's information.

        Serializes and returns authenticated user's profile data.

        Args:
            request: HTTP request from authenticated user

        Returns:
            Response containing serialized user data
        """
        user = request.user
        serializer = UserSerializer(instance=user, many=False)
        return Response.success({
            'message': 'User profile retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('POST')

    def put(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        return Response.options(['POST'])
