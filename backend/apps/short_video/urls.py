from django.urls import re_path

from .views.tag_view import TagDetailView, TagListView
from .views.short_video_view import (
    ShortVideoListCreateView,
    ShortVideoChoiceFieldsAPIView,
)

urlpatterns = [
    re_path(r"^tags/?$", TagListView.as_view(), name="tag-list"),
    re_path(r"^tags/<int:tag_id>/?$", TagDetailView.as_view(), name="tag-detail"),
    re_path(
        r"^short-videos/?$",
        ShortVideoListCreateView.as_view(),
        name="short-video-list-create",
    ),
    re_path(
        r"^short-videos/choice-fields/?$",
        ShortVideoChoiceFieldsAPIView.as_view(),
        name="short-video-choice-fields",
    ),
]
