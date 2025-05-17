from django.urls import path

from .views.tag_view import TagDetailView, TagListView

urlpatterns = [
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/<int:tag_id>/", TagDetailView.as_view(), name="tag-detail"),
]
