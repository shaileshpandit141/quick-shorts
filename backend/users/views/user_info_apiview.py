# Django imports
from django.contrib.auth import get_user_model

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# Local imports
from permissions import IsAuthenticated, IsVerified
from throttles import UserRateThrottle
from utils import Response, FieldValidator
from users.serializers import UserSerializer

User = get_user_model()


class UserInfoAPIView(APIView):
    """
    API View for managing authenticated user information.

    Provides endpoints to retrieve and update user profile data.
    Authentication and verification required for all operations.

    Methods:
        get: Retrieve user information
        post: Not allowed
        put: Not allowed
        patch: Update user information
        delete: Not allowed
        options: Get allowed methods

    Attributes:
        permission_classes: Requires authenticated and verified user
        throttle_classes: Rate limits requests for authenticated users
    """
    permission_classes = [IsAuthenticated, IsVerified]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """
        Retrieve current user's profile information.

        Args:
            request: HTTP request object containing authenticated user

        Returns:
            Response: JSON response with user data and success message
        """
        user = request.user
        serializer = UserSerializer(instance=user, many=False)
        return Response.success({
            'message': 'User profile retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> Response.type:
        """Not supported - returns method not allowed response"""
        return Response.method_not_allowed('POST')

    def put(self, request, *args, **kwargs) -> Response.type:
        """Not supported - returns method not allowed response"""
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """
        Update authenticated user's profile information.

        Validates and updates first name and last name fields.

        Args:
            request: HTTP request containing user data updates

        Returns:
            Response: JSON response with updated data or validation errors
        """
        user = request.user
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name')
        }

        # Validate required fields
        clean_data = FieldValidator(data, ['first_name', 'last_name'])
        if not clean_data.is_valid():
            return Response.error({
                'message': 'Invalid Request',
                'errors': clean_data.get_errors()
            }, status.HTTP_400_BAD_REQUEST)

        # Update user instance with new data
        instance = UserSerializer(
            data=data,
            instance=user,
            many=False,
            partial=True
        )

        if not instance.is_valid():
            return Response.error({
                'message': 'Oops! Something went wrong',
                'errors': {
                    'non_field_errors': [
                        'Something went wrong. Please try again later.'
                    ]
                }
            }, status.HTTP_400_BAD_REQUEST)

        instance.save()
        return Response.success({
            'message': 'User profile updated successfully',
            'data': instance.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs) -> Response.type:
        """Not supported - returns method not allowed response"""
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """Return allowed HTTP methods for this endpoint."""
        return Response.options(['POST', 'PATCH'])
