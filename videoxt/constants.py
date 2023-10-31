"""Contains constants used throughout the libary and version information."""
import importlib.metadata
from enum import Enum

import cv2  # type: ignore

VERSION = importlib.metadata.version("videoxt")


class ExtractionMethod(Enum):
    """
    Enumeration of the supported extraction methods: audio, clip, frames, gif.

    Attributes:
    -----
        `AUDIO` (str):
            Extract the audio from a video file.
        `CLIP` (str):
            Extract a clip from a video file.
        `FRAMES` (str):
            Extract frames from a video file.
        `GIF` (str):
            Create a GIF from a video file.
    """

    AUDIO = "audio"
    CLIP = "clip"
    FRAMES = "frames"
    GIF = "gif"


SUPPORTED_VIDEO_FORMATS = {
    "3gp",
    "asf",
    "avi",
    "divx",
    "flv",
    "m4v",
    "mkv",
    "mov",
    "mp4",
    "mpeg",
    "mpg",
    "ogv",
    "rm",
    "ts",
    "vob",
    "webm",
    "wmv",
}

SUPPORTED_AUDIO_FORMATS = {
    "m4a",
    "mp3",
    "ogg",
    "wav",
}

SUPPORTED_IMAGE_FORMATS = {
    "bmp",
    "dib",
    "jp2",
    "jpeg",
    "jpg",
    "png",
    "tif",
    "tiff",
    "webp",
}

VALID_ROTATE_VALUES = {0, 90, 180, 270}

ROTATION_MAP = {
    90: cv2.ROTATE_90_CLOCKWISE,
    180: cv2.ROTATE_180,
    270: cv2.ROTATE_90_COUNTERCLOCKWISE,
}
