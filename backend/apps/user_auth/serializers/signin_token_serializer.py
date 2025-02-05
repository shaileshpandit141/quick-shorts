from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SigninTokenSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to issue JWT tokens for users, replacing the username
    field with email for authentication.
    """

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            if not user:
                raise AuthenticationFailed("Invalid email or password")

            if not user.is_active:
                raise AuthenticationFailed("Account is disabled")

            data = super().validate(attrs)
            data.update({"user": user})
            return data

        raise AuthenticationFailed("Email and password must be provided")
