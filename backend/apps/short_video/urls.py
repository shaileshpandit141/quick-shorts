from rest_framework.routers import DefaultRouter

from .views.short_video_view import ShortVideoModelViewSet
from .views.tag_view import TagModelViewSet
from .views.short_video_view_view import ShortVideoViewModelViewSet

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

# Include the router's URLs in the urlpatterns
urlpatterns += router.urls
