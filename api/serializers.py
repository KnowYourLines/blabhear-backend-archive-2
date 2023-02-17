from rest_framework.fields import FileField, CharField, ChoiceField
from rest_framework.serializers import Serializer


class VideoNoteInputSerializer(Serializer):
    audio = FileField()
    transcript = CharField(allow_blank=True)
    effect = ChoiceField(
        choices=[
            "High Pitch",
            "Low Pitch",
            "Wobble",
            "Echo",
            "Fuzzy",
            "Hyper",
            "Sleepy",
        ],
        allow_blank=True,
    )


class TranscribeInputSerializer(Serializer):
    audio = FileField()
