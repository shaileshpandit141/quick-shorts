from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.comment import CommentModelViewSet
from .views.follow import FollowModelViewSet
from .views.like import LikeModelViewSet
from .views.report import ReportModelViewSet
from .views.video_stream import VideoStreamAPIView
from .views.video import VideoModelViewSet
from .views.tag import TagModelViewSet
from .views.view import ViewModelViewSet

# Define empty urlpatterns
urlpatterns = [
    # Add short videos streams endpoint
    path(
        "videos/streams/<int:video_id>/",
        VideoStreamAPIView.as_view(),
        name="videos-stream",
    )
]

# Create a default Drf router
router = DefaultRouter()

# Register the ShortVideoModelViewSet with the router
router.register(r"videos", VideoModelViewSet, basename="video")

# Register the TagModelViewSet with the router
router.register(r"tags", TagModelViewSet, basename="tag")

# Register the ViewModelViewSet with the router
router.register(r"views", ViewModelViewSet, basename="view")

# Register the LikeModelViewSet with the router
router.register(r"likes", LikeModelViewSet, basename="like")

# Register the FollowModelViewSet with the router
router.register(r"follows", FollowModelViewSet, basename="follow")

# Register the CommentModelViewSet with the router
router.register(r"comments", CommentModelViewSet, basename="comment")

# Register the ReportModelViewSet with the router
router.register(r"reports", ReportModelViewSet, basename="report")

# Include the router's URLs in the urlpatterns
urlpatterns += router.urls
