"""Configuration settings for video generation"""

# Video settings
DEFAULT_DURATION = 60  # seconds
DEFAULT_FPS = 30
DEFAULT_RESOLUTION = "1920x1080"
VIDEO_QUALITY_CRF = 18  # Lower = better quality (18-28 range)

# Audio settings
AUDIO_BITRATE = "192k"
VOICE_OPTIONS = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
DEFAULT_VOICE = "alloy"

# Style presets
STYLES = {
    "professional": {
        "tone": "professional and polished",
        "pacing": "moderate",
        "music": "corporate, uplifting"
    },
    "casual": {
        "tone": "friendly and conversational",
        "pacing": "relaxed",
        "music": "upbeat, fun"
    },
    "educational": {
        "tone": "clear and informative",
        "pacing": "steady with pauses",
        "music": "calm, focused"
    },
    "entertaining": {
        "tone": "energetic and engaging",
        "pacing": "fast, dynamic",
        "music": "exciting, dramatic"
    }
}

# Image generation
DALLE_SIZES = ["1024x1024", "1792x1024", "1024x1792"]
DEFAULT_IMAGE_SIZE = "1792x1024"  # 16:9 aspect ratio
IMAGE_QUALITY = "hd"

# Subtitle settings
SUBTITLE_FONT_SIZE = 24
SUBTITLE_COLOR = "white"
SUBTITLE_OUTLINE_COLOR = "black"

# API settings
GPT_MODEL = "gpt-4"
TTS_MODEL = "tts-1-hd"
DALLE_MODEL = "dall-e-3"
