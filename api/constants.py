import os

from deepgram import Deepgram
from pedalboard import Pedalboard
from pedalboard_native import PitchShift, Chorus, Delay

DEEPGRAM_CLIENT = Deepgram(os.environ.get("DEEPGRAM_API_KEY"))
VOICE_EFFECTS = {
    "High Pitch": Pedalboard([PitchShift(5)]),
    "Low Pitch": Pedalboard([PitchShift(-5)]),
    "Wobble": Pedalboard([Chorus(rate_hz=10, mix=1)]),
    "Echo": Pedalboard([Delay(delay_seconds=0.125, feedback=0.75, mix=0.5)]),
    "High Echo": Pedalboard([Delay(delay_seconds=0.125, feedback=0.75, mix=0.5), PitchShift(5)]),
    "Low Echo": Pedalboard([Delay(delay_seconds=0.125, feedback=0.75, mix=0.5), PitchShift(-5)]),
    "High Wobble": Pedalboard([Chorus(rate_hz=10, mix=1), PitchShift(5)]),
    "Low Wobble": Pedalboard([Chorus(rate_hz=10, mix=1), PitchShift(-5)]),
}
LANGUAGES = [
    ("en", "English"),
    ("en-GB", "English (GB)"),
    ("en-US", "English (US)"),
    ("en-AU", "English (AU)"),
    ("en-IN", "English (IN)"),
    ("en-NZ", "English (NZ)"),
    ("fr", "French"),
    ("fr-CA", "French (CA)"),
    ("uk", "Ukrainian"),
    ("es", "Spanish"),
    ("es-419", "Spanish (LatAm)"),
    ("tr", "Turkish"),
    ("ta", "Tamil"),
    ("sv", "Swedish"),
    ("ru", "Russian"),
    ("pt", "Portuguese"),
    ("pt-BR", "Portuguese (BR)"),
    ("pt-PT", "Portuguese (PT)"),
    ("pl", "Polish"),
    ("no", "Norwegian"),
    ("ko", "Korean"),
    ("ja", "Japanese"),
    ("it", "Italian"),
    ("id", "Indonesian"),
    ("hi", "Hindi"),
    ("hi-Latn", "Hindi (Roman)"),
    ("de", "German"),
    ("nl", "Dutch/Flemish"),
    ("da", "Danish"),
    ("zh", "Chinese"),
    ("zh-CN", "Chinese (CN)"),
    ("zh-TW", "Chinese (TW)"),
]
