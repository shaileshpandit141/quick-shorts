# Django imports
from django.contrib.auth import get_user_model

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework_simplejwt.views import TokenRefreshView

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import Response, TokenGenerator

User = get_user_model()


class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('get')

    def post(self, request, *args, **kwargs) -> Response.type:
        token = request.data.get('token', None)

        if token is None:
            return Response.error({
                'message': 'Invalid request',
                'errors': {
                    'token': 'Token can has not be empty'
                }
            }, status.HTTP_400_BAD_REQUEST)

        try:
            data = TokenGenerator.decode(token, 'email_verification_salt')
            user_id = data["user_id"]

            user = User.objects.get(id=user_id)
            if user.is_email_verified:
                return Response.success({
                    'message': 'Email already verified',
                    'data': {
                        'detail': 'Email already verified.'
                    }
                }, status.HTTP_200_OK)

            user.is_email_verified = True
            user.save()
            return Response.success({
                'message': 'Email verified successfully',
                'data': {
                    'detail': 'Email verified successfully'
                }
            }, status.HTTP_200_OK)

        except ValueError as error:
            return Response.error({
                'message': 'Invalid token',
                'errors': {
                    'non_field_errors': [str(error)]
                }
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('put')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('patch')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('delete')

    def options(self, request, *args, **kwargs) -> Response.type:
        return Response.options(['POST'])
