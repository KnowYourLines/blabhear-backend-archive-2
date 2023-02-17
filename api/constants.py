import os

from deepgram import Deepgram
from pedalboard import Pedalboard
from pedalboard_native import PitchShift

DEEPGRAM_CLIENT = Deepgram(os.environ.get("DEEPGRAM_API_KEY"))
VOICE_EFFECTS = {"High Pitch": Pedalboard([PitchShift(5)])}
