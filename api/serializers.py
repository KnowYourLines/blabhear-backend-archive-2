from rest_framework.fields import FileField, CharField, ChoiceField
from rest_framework.serializers import Serializer

from api.constants import VOICE_EFFECTS


class VideoNoteInputSerializer(Serializer):
    audio = FileField()
    transcript = CharField(allow_blank=True)
    effect = ChoiceField(
        choices=list(VOICE_EFFECTS),
        allow_blank=True,
    )


class TranscribeInputSerializer(Serializer):
    audio = FileField()
