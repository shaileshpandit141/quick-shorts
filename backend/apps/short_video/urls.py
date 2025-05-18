from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.short_video_view import ShortVideoModelViewSet
from .views.tag_view import TagDetailView, TagListView

urlpatterns = [
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/<int:tag_id>/", TagDetailView.as_view(), name="tag-detail"),
]

# Create a default Drf router
router = DefaultRouter()

# Register the ShortVideoModelViewSet with the router
router.register(r"short-videos", ShortVideoModelViewSet, basename="short-video")

# Include the router's URLs in the urlpatterns
urlpatterns += router.urls
