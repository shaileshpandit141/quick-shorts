from rest_core.viewsets.mixins import ChoiceFieldViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from short_video.models.report import Report
from short_video.serializers.report_serializer import ReportSerializer


class ReportModelViewSet(
    ChoiceFieldViewSetMixin,
    ModelViewSet,
):
    """Report view CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_field = "id"

    def perform_create(self, serializer) -> None:
        """Create a new report view with the user."""
        serializer.save(reported_by=self.request.user)
