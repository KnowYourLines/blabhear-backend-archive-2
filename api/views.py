import tempfile
import textwrap

from PIL import ImageFont, Image, ImageDraw
from django.http import FileResponse
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from pedalboard_native.io import AudioFile
from pydub import AudioSegment
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.constants import VOICE_EFFECTS, DEEPGRAM_CLIENT, BASE_TIER_LANGUAGES
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

        img_width = 512
        img_height = 512
        txt_start_height = 20
        txt_start_width = 20
        font = ImageFont.truetype("arial-unicode-ms.ttf", size=24)
        img = Image.new("RGB", (img_width, img_height), color="blue")
        img_draw = ImageDraw.Draw(img)
        img_draw.textsize(transcript, font=font)
        txt_height = txt_start_height
        lines = textwrap.wrap(transcript, width=40)
        for line in lines:
            line_width, line_height = font.getsize(line)
            img_draw.text(
                (txt_start_width, txt_height), line, font=font, fill=(255, 255, 0)
            )
            txt_height += line_height
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

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        return serializer_class(*args, **kwargs)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audio = serializer.validated_data["audio"]
        language = serializer.validated_data["language"]
        source = {"buffer": audio, "mimetype": "audio/ogg"}
        options = {
            "punctuate": True,
            "model": "general",
            "language": language,
            "tier": "enhanced" if language not in BASE_TIER_LANGUAGES else "base",
        }
        response = DEEPGRAM_CLIENT.transcription.sync_prerecorded(source, options)
        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        return Response({"transcript": transcript})
