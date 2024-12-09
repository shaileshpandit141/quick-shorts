# Django REST framework imports
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

# Local imports
from permissions import IsAuthenticated
from throttles import UserRateThrottle
from utils import Response, FieldValidator


class SignoutAPIView(APIView):
    """API view for listing and creating YourModel instances.

    Supports GET and POST methods. Other HTTP methods return 400 errors.
    Requires authentication and implements rate limiting.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """Retrieve YourModel instances for the authenticated user."""
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        """Create one or more new YourModel instances."""
        clean_data = FieldValidator(request.data, ['refresh_token'])
        if not clean_data.is_valid():
            return Response.error({
                'message': 'Invalid Request',
                'errors': clean_data.get_errors()
            })

        token = RefreshToken(clean_data.get('refresh_token'))
        # Blacklist the token
        token.blacklist()
        return Response.success({
            'message': 'Sign out successful',
            'data': {
                'detail': 'Token successfully blacklisted.'
            }
        }, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs) -> Response.type:
        """PUT method not supported."""
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """PATCH method not supported."""
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        """DELETE method not supported."""
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """OPTIONS method not supported."""
        return Response.options(['POST'])
