import argparse
import os
import re
from pathlib import Path
from typing import Tuple
from typing import Union

import videoxt.constants as C
import videoxt.utils as utils


class ValidationException(Exception):
    pass


def _raise_error(error_msg: str) -> None:
    if C.IS_TERMINAL:
        raise argparse.ArgumentTypeError(error_msg)
    raise ValidationException(error_msg)


def positive_int(num: Union[float, int, str]) -> int:
    try:
        value = float(num)
    except ValueError:
        _raise_error(f"expected integer, got {num!r}")

    if not value.is_integer():
        _raise_error(f"expected integer, got {num!r}")

    if value <= 0:
        _raise_error(f"expected positive integer, got {num}")

    return int(value)


def positive_float(num: Union[float, int, str]) -> float:
    try:
        value = float(num)
    except ValueError:
        _raise_error(f"expected numeric value, got {num!r}")

    if value <= 0:
        _raise_error(f"expected positive number, got {num}")

    return value


def non_negative_int(num: Union[float, int, str]) -> int:
    try:
        value = float(num)
    except ValueError:
        _raise_error(f"expected integer, got {num!r}")

    if not value.is_integer():
        _raise_error(f"expected integer, got {num!r}")

    if value < 0:
        _raise_error(f"expected non-negative integer, got {num}")

    return int(value)


def non_negative_float(num: Union[int, float, str]) -> float:
    try:
        value = float(num)
    except ValueError:
        _raise_error(f"expected numeric value, got {num!r}")

    if value < 0:
        _raise_error(f"expected non-negative number, got {num}")

    return value


def valid_filepath(filepath: Union[str, Path]) -> str:
    filepath = str(filepath)
    if not os.path.isfile(filepath):
        _raise_error(f"file not found, got {filepath!r}")

    return filepath


def valid_dir(dir: Union[str, Path]) -> str:
    dir = str(dir)
    if not os.path.exists(dir):
        _raise_error(f"directory not found, got {dir!r}")

    if not os.path.isdir(dir):
        _raise_error(f"expected directory, got {dir!r}")

    return dir


def valid_filename(filename: str) -> str:
    invalid_chars = r"[\\/:*?\"<>|]"

    if re.search(invalid_chars, filename):
        _raise_error(
            f"invalid filename, got {filename!r}\n"
            f"filename can't contain any of the following characters: \\/:*?\"<>|"
        )

    return filename


def valid_image_format(image_format: str) -> str:
    image_format = str(image_format).lower().strip(".")
    if image_format not in C.VALID_IMAGE_FORMATS:
        _raise_error(
            f"invalid image format, got {image_format!r}\n"
            f"valid image formats: {C.VALID_IMAGE_FORMATS}"
        )

    return image_format


def valid_timestamp(timestamp: str, timestamp_type: str) -> str:
    timestamp_as_seconds = None
    if ":" in timestamp:
        regex = r"^([0-9]|[0-5][0-9])(:[0-5][0-9]){1,2}$"
        if not bool(re.match(regex, timestamp)):
            _raise_error(f"invalid timestamp, got {timestamp!r}")

        timestamp_as_seconds = utils.timestamp_to_seconds(timestamp)

    if timestamp_type == "start":
        timestamp_as_seconds = (
            non_negative_float(timestamp)
            if timestamp_as_seconds is None
            else non_negative_float(timestamp_as_seconds)
        )
    elif timestamp_type == "stop":
        timestamp_as_seconds = (
            positive_float(float(timestamp))
            if timestamp_as_seconds is None
            else positive_float(timestamp_as_seconds)
        )

    return timestamp


def valid_resize_value(resize_value: Union[float, str]) -> float:
    """Video resize mutliplier max value of 50 is arbitrary, but is used to prevent
    the user from accidentally resizing output to abnormally large size.
    """
    try:
        resize_value = float(resize_value)
    except ValueError:
        _raise_error(f"invalid resize value, got {resize_value!r}")

    if not 0.01 <= resize_value <= 50:
        _raise_error(f"resize value must be between 0.01 and 50, got {resize_value}")

    return resize_value


def valid_dimensions(dimensions: Tuple[int, int]) -> Tuple[int, int]:
    """Dimensions are validated differently when run from command-line because
    argparse's type conversions are applied to each argument individually.
    """
    if len(dimensions) != 2:
        _raise_error(f"invalid dimensions, got {dimensions!r}")

    dimensions = tuple([positive_int(dim) for dim in list(dimensions)])

    return dimensions


def valid_rotate_value(rotate_value: Union[int, str]) -> int:
    """Valid rotate values are 0, 90, 180, 270."""
    try:
        rotate_value = int(rotate_value)
    except ValueError:
        _raise_error(
            f"invalid rotate value, got {rotate_value!r}\n"
            f"valid rotate values: {C.VALID_ROTATE_VALUES}"
        )

    if rotate_value not in C.VALID_ROTATE_VALUES:
        _raise_error(
            f"invalid rotate value, got {rotate_value!r}\n"
            f"valid rotate values: {C.VALID_ROTATE_VALUES}"
        )

    return rotate_value


def valid_start_time(start_time: Union[float, int, str]) -> Union[float, int, str]:
    if isinstance(start_time, int):
        start_time = non_negative_int(start_time)
        return start_time

    if isinstance(start_time, float):
        start_time = non_negative_float(start_time)
        return start_time

    if isinstance(start_time, str):
        start_time = valid_timestamp(start_time, timestamp_type="start")
        return start_time

    _raise_error(f"invalid start time, got {start_time!r}")


def valid_stop_time(stop_time: Union[float, int, str]) -> Union[float, int, str]:
    if isinstance(stop_time, int):
        stop_time = positive_int(stop_time)
        return stop_time

    if isinstance(stop_time, float):
        stop_time = positive_float(stop_time)
        return stop_time

    if isinstance(stop_time, str):
        stop_time = valid_timestamp(stop_time, timestamp_type="stop")
        return stop_time

    _raise_error(f"invalid stop time, got {stop_time!r}")


def validate_video_extraction_range(
    start_seconds: float, stop_seconds: float, video_length_seconds: float
) -> None:
    if start_seconds > video_length_seconds:
        _raise_error(
            f"start time in seconds ({start_seconds}) exceeds video length in seconds ({video_length_seconds})"
        )

    if start_seconds > stop_seconds:
        _raise_error(
            f"start time in seconds ({start_seconds}) exceeds stop time in seconds ({stop_seconds})"
        )


def valid_capture_rate(capture_rate: int, start_frame: float, stop_frame: float) -> int:
    """Capture rate is validated after determining the start and stop video frames."""
    if capture_rate > (stop_frame - start_frame):
        _raise_error(
            f"capture rate ({capture_rate}) exceeds range between "
            f"start ({start_frame}) and stop ({stop_frame}) frames"
        )

    return capture_rate
