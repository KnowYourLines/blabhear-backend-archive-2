import tempfile

from PIL import ImageFont, Image, ImageDraw
from django.http import FileResponse
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from pedalboard import Pedalboard
from pedalboard_native import PitchShift
from pedalboard_native.io import AudioFile
from pydub import AudioSegment
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
        song = AudioSegment.from_file(audio)
        tmp_mp3 = tempfile.NamedTemporaryFile(suffix=".mp3")
        song.export(tmp_mp3.name, format="mp3")
        tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav")

        with AudioFile(tmp_mp3.name) as f:
            audio = f.read(f.frames)
            samplerate = f.samplerate

            # Make a Pedalboard object, containing multiple plugins:
            board = Pedalboard([PitchShift(5)])

            # Run the audio through this pedalboard!
            effected = board(audio, samplerate)

            # Write the audio back as a wav file:
            with AudioFile(tmp_wav.name, "w", samplerate, effected.shape[0]) as f:
                f.write(effected)

        width = 512
        height = 512
        message = "Hello boss!"
        font = ImageFont.truetype("arial.ttf", size=24)
        img = Image.new("RGB", (width, height), color="blue")
        img_draw = ImageDraw.Draw(img)
        img_draw.textsize(message, font=font)
        img_draw.text((10, 10), message, font=font, fill=(255, 255, 0))
        tmp_img = tempfile.NamedTemporaryFile(suffix=".png")
        img.save(tmp_img.name)

        audio = AudioFileClip(tmp_wav.name)
        clip = ImageClip(tmp_img.name).set_duration(audio.duration)
        clip = clip.set_audio(audio)
        tmp_vid = tempfile.NamedTemporaryFile(suffix=".mp4")
        clip.write_videofile(tmp_vid.name, fps=1, logger=None)

        response = FileResponse(tmp_vid)
        return response


class TranscribeViewSet(ViewSet):
    pass


class VoiceChangerViewSet(ViewSet):
    pass
