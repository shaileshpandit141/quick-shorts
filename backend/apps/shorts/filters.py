from django_filters import CharFilter, FilterSet
from shorts.models.video import Video


class VideoFilterSet(FilterSet):
    username = CharFilter(field_name="owner__username", lookup_expr="iexact")
    tag = CharFilter(field_name="tags__name", lookup_expr="iexact")

    class Meta:
        model = Video
        fields = ["username", "tag"]
