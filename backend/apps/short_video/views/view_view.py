from rest_core.viewsets.mixins import ChoiceFieldViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from short_video.models.view import View
from short_video.serializers.view_serializer import ViewSerializer


class ViewModelViewSet(
    ChoiceFieldViewSetMixin,
    ModelViewSet,
):
    """Short video view CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = View.objects.all()
    serializer_class = ViewSerializer
    lookup_field = "id"

    def perform_create(self, serializer) -> None:
        """Create a new short video view with the user."""
        serializer.save(user=self.request.user)
