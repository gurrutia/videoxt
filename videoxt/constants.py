import importlib.metadata

import cv2  # type: ignore

VERSION = importlib.metadata.version("videoxt")

VALID_ROTATE_VALUES = (0, 90, 180, 270)

ROTATION_MAP = {
    90: cv2.ROTATE_90_CLOCKWISE,
    180: cv2.ROTATE_180,
    270: cv2.ROTATE_90_COUNTERCLOCKWISE,
}


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
