from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SigninTokenSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to issue JWT tokens for users, replacing the username
    field with email for authentication.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        # Authenticate the user
        credentials = {
            'email': attrs['email'],
            'password': attrs['password'],
        }

        user = authenticate(**credentials)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('This account is inactive')

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        # Include user in the validated data
        return {
            'user': user,
            'access': str(refresh.access_token),  # type: ignore
            'refresh': str(refresh),
        }
