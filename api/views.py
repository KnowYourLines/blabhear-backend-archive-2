from django.http import FileResponse
from rest_framework.viewsets import ViewSet

from api.serializers import UploadSerializer


class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def create(self, request):
        file_uploaded = request.FILES.get("file_uploaded")
        response = FileResponse(file_uploaded)
        return response
