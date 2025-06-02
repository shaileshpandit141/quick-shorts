from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from shorts.models.report import Report
from shorts.serializers.report import ReportSerializer


class ReportModelViewSet(ModelViewSet):
    """Report view CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_field = "id"
    http_method_names = ["post"]

    def perform_create(self, serializer) -> None:
        """Create a new report view with the user."""
        serializer.save(reported_by=self.request.user)
