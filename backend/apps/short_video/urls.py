from rest_framework.routers import DefaultRouter

from .views.comment_view import CommentModelViewSet
from .views.follow_view import FollowModelViewSet
from .views.like_view import LikeModelViewSet
from .views.report_view import ReportModelViewSet
from .views.short_video_view import ShortVideoModelViewSet
from .views.tag_view import TagModelViewSet
from .views.view_view import ViewModelViewSet

# Define empty urlpatterns
urlpatterns = []

# Create a default Drf router
router = DefaultRouter()

# Register the ShortVideoModelViewSet with the router
router.register(r"short-videos", ShortVideoModelViewSet, basename="short-video")

# Register the TagModelViewSet with the router
router.register(r"tags", TagModelViewSet, basename="tag")

# Register the ViewModelViewSet with the router
router.register(r"views", ViewModelViewSet, basename="view")

# Register the LikeModelViewSet with the router
router.register(r"likes", LikeModelViewSet, basename="like")

# Register the FollowModelViewSet with the router
router.register(r"followers", FollowModelViewSet, basename="follower")

# Register the CommentModelViewSet with the router
router.register(r"comments", CommentModelViewSet, basename="comment")

# Register the ReportModelViewSet with the router
router.register(r"reports", ReportModelViewSet, basename="report")

# Include the router's URLs in the urlpatterns
urlpatterns += router.urls
