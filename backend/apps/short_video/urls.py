from rest_framework.routers import DefaultRouter

from .views.comment_view import CommentModelViewSet
from .views.follow_view import FollowViewModelViewSet
from .views.like_view import LikeViewModelViewSet
from .views.report_view import ReportModelViewSet
from .views.short_video_view import ShortVideoModelViewSet
from .views.short_video_view_view import ShortVideoViewModelViewSet
from .views.tag_view import TagModelViewSet

# Define empty urlpatterns
urlpatterns = []

# Create a default Drf router
router = DefaultRouter()

# Register the ShortVideoModelViewSet with the router
router.register(r"short-videos", ShortVideoModelViewSet, basename="short-video")

# Register the TagModelViewSet with the router
router.register(r"tags", TagModelViewSet, basename="tag")

# Register the ShortVideoViewModelViewSet with the router
router.register(r"views", ShortVideoViewModelViewSet, basename="view")

# Register the LikeViewModelViewSet with the router
router.register(r"likes", LikeViewModelViewSet, basename="like")

# Register the FollowViewModelViewSet with the router
router.register(r"followers", FollowViewModelViewSet, basename="follower")

# Register the CommentModelViewSet with the router
router.register(r"comments", CommentModelViewSet, basename="comment")

# Register the ReportModelViewSet with the router
router.register(r"reports", ReportModelViewSet, basename="report")

# Include the router's URLs in the urlpatterns
urlpatterns += router.urls
