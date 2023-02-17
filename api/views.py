import tempfile

from PIL import ImageFont, Image, ImageDraw
from django.http import FileResponse
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from pedalboard_native.io import AudioFile
from pydub import AudioSegment
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.constants import VOICE_EFFECTS, DEEPGRAM_CLIENT
from api.serializers import VideoNoteInputSerializer, TranscribeInputSerializer


class VideoNoteViewSet(ViewSet):
    serializer_class = VideoNoteInputSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        return serializer_class(*args, **kwargs)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audio = serializer.validated_data["audio"]
        transcript = serializer.validated_data["transcript"]
        effect = serializer.validated_data["effect"]
        song = AudioSegment.from_file(audio)
        tmp_mp3 = tempfile.NamedTemporaryFile(suffix=".mp3")
        song.export(tmp_mp3.name, format="mp3")
        vidnote_audio = tmp_mp3
        voice_effect = VOICE_EFFECTS.get(effect)
        if voice_effect:
            tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav")
            vidnote_audio = tmp_wav
            with AudioFile(tmp_mp3.name) as f:
                audio = f.read(f.frames)
                samplerate = f.samplerate

                # Make a Pedalboard object, containing multiple plugins:
                board = voice_effect

                # Run the audio through this pedalboard!
                effected = board(audio, samplerate)

                # Write the audio back as a wav file:
                with AudioFile(tmp_wav.name, "w", samplerate, effected.shape[0]) as f:
                    f.write(effected)

        width = 512
        height = 512
        font = ImageFont.truetype("arial.ttf", size=24)
        img = Image.new("RGB", (width, height), color="blue")
        img_draw = ImageDraw.Draw(img)
        img_draw.textsize(transcript, font=font)
        img_draw.text((10, 10), transcript, font=font, fill=(255, 255, 0))
        tmp_img = tempfile.NamedTemporaryFile(suffix=".png")
        img.save(tmp_img.name)

        audio = AudioFileClip(vidnote_audio.name)
        clip = ImageClip(tmp_img.name).set_duration(audio.duration)
        clip = clip.set_audio(audio)
        tmp_vid = tempfile.NamedTemporaryFile(suffix=".mp4")
        clip.write_videofile(tmp_vid.name, fps=1, logger=None)

        response = FileResponse(tmp_vid)
        return response


class TranscribeViewSet(ViewSet):
    serializer_class = TranscribeInputSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        audio = serializer.validated_data["audio"]
        source = {"buffer": audio, "mimetype": "audio/ogg"}
        options = {
            "punctuate": True,
            "model": "general",
            "language": "en",
            "tier": "base",
        }
        response = DEEPGRAM_CLIENT.transcription.sync_prerecorded(source, options)
        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        return Response({"transcript": transcript})
