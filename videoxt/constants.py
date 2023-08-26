import importlib.metadata


VERSION = importlib.metadata.version("videoxt")


VALID_VIDEO_FORMATS = (
    "mp4",
    "avi",
    "mkv",
    "mov",
    "wmv",
)

VALID_AUDIO_FORMATS = (
    "m4a",
    "mp3",
    "ogg",
    "wav",
)


VALID_IMAGE_FORMATS = (
    "bmp",
    "dib",
    "jpeg",
    "jpg",
    "png",
    "tiff",
    "tif",
    "webp",
)


EMOJI_MAP = {
    "video": "VIDEO \N{FILM PROJECTOR}",
    "extraction": "EXTRACTION \N{TOOTH}",
    "audio": "AUDIO \N{SPEAKER WITH THREE SOUND WAVES}",
    "clip": "CLIP \N{FILM PROJECTOR}",
    "frames": "FRAMES \N{CAMERA WITH FLASH}",
    "gif": "GIF \N{FILM FRAMES}",
}
