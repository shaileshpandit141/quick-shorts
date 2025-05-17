from rest_core.pagination import paginate_and_serialize_data
from rest_core.response import destroy_response, failure_response, success_response
from rest_core.views.mixins import ModelObjectMixin, ModelChoiceFiledMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from short_video.models.short_video import ShortVideo
from short_video.serializers.short_video_serializer import ShortVideoSerializer


class ShortVideoListCreateView(APIView):
    """ShortVideo list Create API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request) -> Response:
        """Get list of short videos"""

        # Get all short videos from the database
        short_videos = ShortVideo.objects.all()

        # Serialize and paginate the short videos
        short_videos = paginate_and_serialize_data(
            request=request,
            queryset=ShortVideo.objects.all(),
            serializer_class=ShortVideoSerializer,
        )

        # Return success response with serialized short videos
        return success_response(
            message="Short videos retrieved successfully",
            data=short_videos,
        )

    def post(self, request) -> Response:
        """Create a new short video"""

        # Serialize the request data
        serializer = ShortVideoSerializer(
            data=request.data,
            many=isinstance(request.data, list),
            context={"request": request},
        )

        # Vlidate the serializer
        if not serializer.is_valid():
            # Return failure response with validation errors
            return failure_response(
                message="Failed to create short video",
                errors=serializer.errors,
            )

        # Save the serializer data to create a new short video
        serializer.save()

        # Return success response with created short video data
        return success_response(
            message="Short video created successfully",
            data=serializer.data,
        )


class ShortVideoChoiceFieldsAPIView(ModelChoiceFiledMixin, APIView):
    """ShortVideo choice fields list API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = ShortVideo.objects.all()
    choice_fields = ["privacy"]

    def get(self, request) -> Response:
        """Get choice fields for ShortVideo model"""
        choice_fields = self.get_choice_fields()

        # Return success response with choice fields
        return success_response(
            message="ShortVideo choice fields retrieved successfully",
            data=choice_fields,
        )
