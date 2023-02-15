from django.http import FileResponse
from rest_framework.viewsets import ViewSet

from api.serializers import VideoNoteInputSerializer


class VideoNoteViewSet(ViewSet):
    serializer_class = VideoNoteInputSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        audio = serializer.validated_data["audio"]
        transcript = serializer.validated_data["transcript"]
        print(transcript)
        response = FileResponse(audio)
        return response
