from django.contrib.postgres.forms.hstore import ValidationError
from core.serializers import BaseModelSerializer
from user_auth.models import User


class UserSerializer(BaseModelSerializer):
    """Serializer for User model that handles serialization and
    deserialization of User objects.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "is_verified",
            "is_staff",
            "is_superuser",
        ]
        read_only_fields = ["id", "usename", "is_verified", "is_staff", "is_superuser"]

    def create(self, validated_data) -> User:
        hashed_password = self.context.get("hashed_password", None)

        email = validated_data.get("email")
        username = email.split("@")[0]

        if hashed_password is None:
            raise ValidationError("Provieded password is not valid.")

        # Handle the single record.
        return User.objects.create(
            password=hashed_password, username=username, **validated_data
        )


class UserUpdateSerializer(BaseModelSerializer):
    """Serializer for User model that handles serialization and
    deserialization of User objects.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar"]
