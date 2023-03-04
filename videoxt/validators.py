import argparse
import os
import re
from typing import Tuple, Union

import videoxt.constants as C
import videoxt.utils as utils


class ValidationException(Exception):
    pass


def positive_int(num: Union[int, str]) -> int:
    error_msg_value = f"expected integer, got {num!r}"

    try:
        value = int(num)
    except ValueError:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_value)
        raise ValidationException(error_msg_value)

    error_msg_positive = f"expected positive integer, got {num}"
    if value <= 0:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_positive)
        raise ValidationException(error_msg_positive)

    return value


def positive_float(num: Union[float, str]) -> float:
    error_msg_value = f"expected numeric value, got {num!r}"

    try:
        value = float(num)
    except ValueError:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_value)
        raise ValidationException(error_msg_value)

    error_msg_positive = f"expected positive number, got {num}"

    if value <= 0:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_positive)
        raise ValidationException(error_msg_positive)

    return value


def non_negative_int(num: Union[int, str]) -> int:
    error_msg_value = f"expected integer, got {num!r}"

    try:
        value = int(num)
    except ValueError:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_value)
        raise ValidationException(error_msg_value)

    error_msg_non_negative = f"expected non-negative integer, got {num}"

    if value < 0:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_non_negative)
        raise ValidationException(error_msg_non_negative)

    return value


def non_negative_float(num: Union[int, float, str]) -> float:
    error_msg_value = f"expected numeric value, got {num!r}"

    try:
        value = float(num)
    except ValueError:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_value)
        raise ValidationException(error_msg_value)

    error_msg_non_negative = f"expected non-negative number, got {num}"

    if value < 0:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_non_negative)
        raise ValidationException(error_msg_non_negative)

    return value


def valid_filepath(filepath: str) -> str:
    error_msg = f"file not found, got {filepath!r}"

    if not os.path.isfile(filepath):
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg)
        raise ValidationException(error_msg)

    return filepath


def valid_dir(dir: str) -> str:
    error_msg_not_found = f"directory not found, got {dir!r}"

    if not os.path.exists(dir):
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_not_found)
        raise ValidationException(error_msg_not_found)

    error_msg_not_dir = f"expected directory, got {dir!r}"

    if not os.path.isdir(dir):
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_not_dir)
        raise ValidationException(error_msg_not_dir)

    return dir


def valid_filename(filename: str) -> str:
    error_msg = (
        f"invalid filename, got {filename!r}\n"
        f"filename can't contain any of the following characters: \\/:*?\"<>|"
    )

    invalid_chars = r"[\\/:*?\"<>|]"

    if re.search(invalid_chars, filename):
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg)
        raise ValidationException(error_msg)

    return filename


def valid_image_format(image_format: str) -> str:
    error_msg = (
        f"invalid image format, got {image_format!r}\n"
        f"valid image formats: {C.VALID_IMAGE_FORMATS}"
    )

    image_format = str(image_format).lower().strip(".")
    if image_format not in C.VALID_IMAGE_FORMATS:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg)
        raise ValidationException(error_msg)

    return image_format


def valid_timestamp(timestamp: str, timestamp_type: str) -> str:
    error_msg = f"invalid timestamp, got {timestamp!r}"

    timestamp_as_seconds = None
    if ":" in timestamp:
        regex = r"^([0-9]|[0-5][0-9])(:[0-5][0-9]){1,2}$"
        if not bool(re.match(regex, timestamp)):
            if C.IS_TERMINAL:
                raise argparse.ArgumentTypeError(error_msg)
            raise ValidationException(error_msg)

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
    error_msg_value = f"invalid resize value, got {resize_value!r}"

    try:
        resize_value = float(resize_value)
    except ValueError:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_value)
        raise ValidationException(error_msg_value)

    error_msg_range = f"resize value must be between 0.01 and 50, got {resize_value}"
    if not 0.01 <= resize_value <= 50:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg_range)
        raise ValidationException(error_msg_range)

    return resize_value


def valid_dimensions(dimensions: Tuple[int, int]) -> Tuple[int, int]:
    """Dimensions are validated differently when run from command-line because
    argparse's type conversions are applied to each argument individually.
    """
    if len(dimensions) != 2:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(f"invalid dimensions, got {dimensions!r}")
        raise ValidationException(f"invalid dimensions, got {dimensions!r}")

    dimensions = tuple([positive_int(dim) for dim in list(dimensions)])

    return dimensions


def valid_rotate_value(rotate_value: Union[int, str]) -> int:
    """Valid rotate values are 0, 90, 180, 270."""
    error_msg = (
        f"invalid rotate value, got {rotate_value!r}\n"
        f"valid rotate values: {C.VALID_ROTATE_VALUES}"
    )

    try:
        rotate_value = int(rotate_value)
    except ValueError:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg)
        raise ValidationException(error_msg)

    if rotate_value not in C.VALID_ROTATE_VALUES:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg)
        raise ValidationException(error_msg)

    return rotate_value


def valid_start_time(start_time: Union[float, int, str]) -> Union[float, int, str]:
    error_msg = f"invalid start time, got {start_time!r}"

    if isinstance(start_time, int):
        start_time = non_negative_int(start_time)
        return start_time

    if isinstance(start_time, float):
        start_time = non_negative_float(start_time)
        return start_time

    if isinstance(start_time, str):
        start_time = valid_timestamp(start_time, timestamp_type="start")
        return start_time

    if C.IS_TERMINAL:
        raise argparse.ArgumentTypeError(error_msg)
    raise ValidationException(error_msg)


def valid_stop_time(stop_time: Union[float, int, str]) -> Union[float, int, str]:
    error_msg = f"invalid stop time, got {stop_time!r}"

    if isinstance(stop_time, int):
        stop_time = positive_int(stop_time)
        return stop_time

    if isinstance(stop_time, float):
        stop_time = positive_float(stop_time)
        return stop_time

    if isinstance(stop_time, str):
        stop_time = valid_timestamp(stop_time, timestamp_type="stop")
        return stop_time

    if C.IS_TERMINAL:
        raise argparse.ArgumentTypeError(error_msg)
    raise ValidationException(error_msg)


def validate_video_extraction_range(
    start_seconds: float, stop_seconds: float, video_length_seconds: float
) -> None:
    error_msg = f"start time in seconds ({start_seconds}) exceeds video length in seconds ({video_length_seconds})"
    if start_seconds > video_length_seconds:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg)
        raise ValidationException(error_msg)

    error_msg = f"start time in seconds ({start_seconds}) exceeds stop time in seconds ({stop_seconds})"
    if start_seconds > stop_seconds:
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg)
        raise ValidationException(error_msg)


def valid_capture_rate(capture_rate: int, start_frame: float, stop_frame: float) -> int:
    """Capture rate is validated after determining the start and stop video frames."""
    error_msg = (
        f"capture rate ({capture_rate}) exceeds range between "
        f"start ({start_frame}) and stop ({stop_frame}) frames"
    )

    if capture_rate > (stop_frame - start_frame):
        if C.IS_TERMINAL:
            raise argparse.ArgumentTypeError(error_msg)
        raise ValidationException(error_msg)

    return capture_rate
