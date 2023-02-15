from rest_framework.fields import FileField, CharField
from rest_framework.serializers import Serializer


class VideoNoteInputSerializer(Serializer):
    audio = FileField()
    transcript = CharField(allow_blank=True)

