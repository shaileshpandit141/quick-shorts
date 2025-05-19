from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_core.views.mixins import ModelObjectMixin
from django.http import StreamingHttpResponse, HttpResponseNotFound
from wsgiref.util import FileWrapper
import os

from short_video.models.short_video import ShortVideo


class ShortVideoStreamAPIView(ModelObjectMixin[ShortVideo], APIView):
    """View to handle short videos stream"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = ShortVideo.objects.all()

    def get(self, request, video_id) -> HttpResponseNotFound | StreamingHttpResponse:
        video_obj = self.get_object(id=video_id)
        if video_obj is None:
            return HttpResponseNotFound("Video file not found.")

        file_path = video_obj.video.path
        file_size = os.path.getsize(file_path)
        range_header = request.headers.get("Range", "").strip()
        content_type = "video/mp4"
        file = open(file_path, "rb")

        if range_header:
            # Parse byte range
            start, end = 0, file_size - 1
            match = range_header.replace("bytes=", "").split("-")
            if match[0]:
                start = int(match[0])
            if len(match) > 1 and match[1]:
                end = int(match[1])
            length = end - start + 1

            file.seek(start)
            response = StreamingHttpResponse(
                FileWrapper(file, blksize=8192), status=206, content_type=content_type
            )
            response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            response["Content-Length"] = str(length)
        else:
            response = StreamingHttpResponse(
                FileWrapper(file, blksize=8192), content_type=content_type
            )
            response["Content-Length"] = str(file_size)

        response["Accept-Ranges"] = "bytes"
        response["Content-Disposition"] = (
            f'inline; filename="{os.path.basename(file_path)}"'
        )
        return response
