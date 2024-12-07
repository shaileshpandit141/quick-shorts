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


class VerifyEmailConfirmAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        token = request.data.get('token', None)
        token_salt = request.data.get('token_salt', None)

        if token is None or token_salt is None:
            errors = {}
            if token is None:
                errors['token'] = ['Token `token` can has not be empty']
            if token_salt is None:
                errors['token_salt'] = ['Token salt `token_salt` can has not be empty']

            return Response.error({
                'message': 'Invalid request',
                'errors': errors
            }, status.HTTP_400_BAD_REQUEST)

        try:
            data = TokenGenerator.decode(token, token_salt)
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
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        return Response.options(['POST'])
