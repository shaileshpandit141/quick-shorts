from django_filters import FilterSet, CharFilter
from short_video.models.short_video import ShortVideo


class ShortVideoFilterSet(FilterSet):
    username = CharFilter(
        field_name="owner__username", lookup_expr="exact"
    )
    tag = CharFilter(
        field_name="tags__name", lookup_expr="exact"
    )

    class Meta:
        model = ShortVideo
        fields = ["username", "tag"]
