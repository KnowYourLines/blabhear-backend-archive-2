from rest_framework.fields import FileField
from rest_framework.serializers import Serializer


class UploadSerializer(Serializer):
    file_uploaded = FileField()

    class Meta:
        fields = ["file_uploaded"]
