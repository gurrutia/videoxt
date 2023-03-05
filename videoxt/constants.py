import importlib.metadata

import cv2

VERSION = importlib.metadata.version("videoxt")

IS_TERMINAL = False

VALID_ROTATE_VALUES = (0, 90, 180, 270)

ROTATION_MAP = {
    90: cv2.ROTATE_90_CLOCKWISE,
    180: cv2.ROTATE_180,
    270: cv2.ROTATE_90_COUNTERCLOCKWISE,
}

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
    "image": "IMAGES \N{CAMERA WITH FLASH}",
    "gif": "GIF \N{FILM FRAMES}",
    "resize_small": "\N{BUG}",
    "resize_normal": "\N{GOAT}",
    "resize_large": "\N{WHALE}",
    "speed_slow": "\N{TURTLE}",
    "speed_normal": "\N{MONKEY}",
    "speed_fast": "\N{RABBIT}",
    "stop": "\N{RAISED HAND}",
    "start": "\N{CLAPPER BOARD}",
    0: "\N{UPWARDS BLACK ARROW}",
    90: "\N{BLACK RIGHTWARDS ARROW}",
    180: "\N{DOWNWARDS BLACK ARROW}",
    270: "\N{LEFTWARDS BLACK ARROW}",
}
