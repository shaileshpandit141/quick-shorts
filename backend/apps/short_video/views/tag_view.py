from rest_core.pagination import paginate_and_serialize_data
from rest_core.response import destroy_response, failure_response, success_response
from rest_core.views.mixins import ModelObjectMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from short_video.models.tag import Tag
from short_video.serializers.tag_serializer import TagSerializer


class TagListView(APIView):
    """View to handle listing and creating tags."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request) -> Response:
        """List all tags."""

        # Get all tags
        tags = Tag.objects.all()

        # Paginate and serialize the tags
        paginated_data = paginate_and_serialize_data(
            request,
            tags,
            TagSerializer,
        )

        # Return the paginated data
        return success_response(
            message="Tags retrieved successfully.",
            data=paginated_data,
        )

    def post(self, request) -> Response:
        """Create a new tag."""

        # Get the serializer with the request data
        serializer = TagSerializer(
            data=request.data,
            many=isinstance(request.data, list),
            context={"request": request},
        )

        # Validate and save the serializer
        if serializer.is_valid():
            tag = serializer.save()

            # Return success response
            return success_response(
                message="Tag created successfully.",
                data=TagSerializer(tag).data,
            )

        # Return failure response if validation fails
        return failure_response(
            message="Failed to create tag.",
            errors=serializer.errors,
        )


class TagDetailView(ModelObjectMixin, APIView):
    """View to handle retrieveing, updating, and deleting a tag."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Tag.objects.all()

    def get(self, request, tag_id) -> Response:
        """Retrieve a tag by ID."""

        # Get the tag object
        tag = self.get_object(id=tag_id)
        if tag is None:
            return failure_response(
                message="Tag not found.",
                errors={"detail": "Tag with this ID does not exist."},
            )

        # Serialize the tag data
        serializer = TagSerializer(instance=tag)

        # Return success response with serialized data
        return success_response(
            message="Tag retrieved successfully.",
            data=serializer.data,
        )

    def put(self, request, tag_id) -> Response:
        """Update a tag by ID."""

        # Get the tag object
        tag = self.get_object(id=tag_id)
        if tag is None:
            return failure_response(
                message="Tag not found.",
                errors={"detail": "Tag with this ID does not exist."},
            )

        # Get the serializer with the request data
        serializer = TagSerializer(instance=tag, data=request.data)

        # Validate and save the serializer
        if serializer.is_valid():
            serializer.save()
            # Return success response with updated data
            return success_response(
                message="Tag updated successfully.",
                data=serializer.data,
            )

        # Return failure response if validation fails
        return failure_response(
            message="Failed to update tag.",
            errors=serializer.errors,
        )

    def delete(self, request, tag_id) -> Response:
        """Delete a tag by ID."""

        # Get the tag object
        tag = self.get_object(id=tag_id)
        if tag is None:
            return failure_response(
                message="Tag not found.",
                errors={"detail": "Tag with this ID does not exist."},
            )

        # Delete the tag
        tag.delete()

        # Return success response
        return destroy_response()
