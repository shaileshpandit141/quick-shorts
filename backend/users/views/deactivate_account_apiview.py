# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# Local imports
from permissions import IsAuthenticated
from throttles import UserRateThrottle
from utils import Response


class DeactivateAccountAPIView(APIView):
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
        user = request.user
        password = request.data.get('password', None)

        if password is None:
            return Response.error({
                'message': 'Invalid Password',
                'errors': {
                    'password': ['password filed is redquired.']
                }
            })

        if not user.check_password(password):
            return Response.error({
                'message': 'Invalid Password',
                'errors': {
                    'password': ['Your password is not currect.']
                }
            })

        user.is_active = False
        user.save()
        return Response.success({
            'message': 'Account deactivation successful',
            'data': {
                'detail': 'Account deactivation successful'
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
