import os

from deepgram import Deepgram
from pedalboard import Pedalboard
from pedalboard_native import PitchShift, Chorus, Delay, Reverb, Gain
from pedalboard_native.utils import Mix

DEEPGRAM_CLIENT = Deepgram(os.environ.get("DEEPGRAM_API_KEY"))
VOICE_EFFECTS = {
    "High Pitch": Pedalboard([PitchShift(5)]),
    "Low Pitch": Pedalboard([PitchShift(-5)]),
    "Wobble": Pedalboard([Chorus(rate_hz=10, mix=0.75)]),
    "Echo": Pedalboard([Delay(delay_seconds=0.125, feedback=0.75, mix=0.5)]),
    "High Echo": Pedalboard(
        [
            PitchShift(5),
            Delay(delay_seconds=0.125, feedback=0.75, mix=0.5),
        ]
    ),
    "Low Echo": Pedalboard(
        [
            PitchShift(-5),
            Delay(delay_seconds=0.125, feedback=0.75, mix=1),
        ]
    ),
    "High Wobble": Pedalboard([PitchShift(5), Chorus(rate_hz=10, mix=0.75)]),
    "Low Wobble": Pedalboard([PitchShift(-5), Chorus(rate_hz=10, mix=0.75)]),
    "Copycats": Pedalboard(
        [
            Mix(
                [
                    Pedalboard(
                        [
                            PitchShift(-5),
                        ]
                    ),
                    Pedalboard(
                        [
                            PitchShift(-3),
                            Delay(delay_seconds=0.5, mix=1.0),
                        ]
                    ),
                    Pedalboard(
                        [
                            PitchShift(3),
                            Delay(delay_seconds=0.25, mix=1.0),
                        ]
                    ),
                    Pedalboard([PitchShift(5)]),
                ]
            ),
            Reverb(),
        ]
    ),
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
BASE_TIER_LANGUAGES = {
    "zh",
    "zh-CN",
    "zh-TW",
    "en-AU",
    "en-GB",
    "en-IN",
    "en-NZ",
    "fr-CA",
    "hi-Latn",
    "id",
    "ru",
    "tr",
    "uk",
}
