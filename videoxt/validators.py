"""User input validators called from Request objects and command line."""
import argparse
import re
import typing as t
from pathlib import Path

import videoxt.constants as C
import videoxt.utils as U
from videoxt.exceptions import ValidationException


def _raise_error(error_msg: str, from_cli: bool = False) -> None:
    if from_cli:
        raise argparse.ArgumentTypeError(error_msg)
    raise ValidationException(error_msg)


def positive_int(num: t.Union[float, int, str], from_cli: bool = False) -> int:
    try:
        value = float(num)
    except ValueError:
        _raise_error(f"expected integer, got {num!r}", from_cli)

    if not value.is_integer():
        _raise_error(f"expected integer, got {num}", from_cli)

    if value <= 0:
        _raise_error(f"expected positive integer, got {num}", from_cli)

    return int(value)


def positive_float(num: t.Union[float, int, str], from_cli: bool = False) -> float:
    try:
        value = float(num)
    except ValueError:
        _raise_error(f"expected numeric value, got {num!r}", from_cli)

    if value <= 0:
        _raise_error(f"expected positive number, got {num}", from_cli)

    return value


def non_negative_int(num: t.Union[float, int, str], from_cli: bool = False) -> int:
    try:
        value = float(num)
    except ValueError:
        _raise_error(f"expected integer, got {num!r}", from_cli)

    if not value.is_integer():
        _raise_error(f"expected integer, got {num!r}", from_cli)

    if value < 0:
        _raise_error(f"expected non-negative integer, got {num}", from_cli)

    return int(value)


def non_negative_float(num: t.Union[float, int, str], from_cli: bool = False) -> float:
    try:
        value = float(num)
    except ValueError:
        _raise_error(f"expected numeric value, got {num!r}", from_cli)

    if value < 0:
        _raise_error(f"expected non-negative number, got {num}", from_cli)

    return value


def valid_dir(dir: t.Union[Path, str], from_cli: bool = False) -> Path:
    dir_path = Path(dir)

    if not dir_path.is_dir():
        _raise_error(f"directory not found, got {dir_path!r}", from_cli)

    return dir_path


def valid_filepath(filepath: t.Union[Path, str], from_cli: bool = False) -> Path:
    filepath_path = Path(filepath)

    if not filepath_path.is_file():
        _raise_error(f"file not found, got {filepath_path}", from_cli)

    return filepath_path


def valid_filename(filename: str, from_cli: bool = False) -> str:
    invalid_chars = r"[\\/:*?\"<>|]"
    if re.search(invalid_chars, filename):
        _raise_error(
            f"invalid filename, got {filename!r}\n"
            f"filename can't contain any of the following characters: \\/:*?\"<>|",
            from_cli,
        )

    if not filename:
        _raise_error(f"invalid filename, got {filename!r}", from_cli)

    return filename


def valid_timestamp(timestamp: str, from_cli: bool = False) -> str:
    """Validates timestamps are in the correct format. Microseconds are ignored.

    Correct formats: `HH:MM:SS`, `H:MM:SS`, `MM:SS`, `M:SS`, `SS`, `S`
    """
    timestamp = timestamp.split(".")[0]

    regex = r"^([0-9]|[0-5][0-9])(:[0-5][0-9]){1,2}$"
    if not bool(re.match(regex, timestamp)):
        _raise_error(f"invalid timestamp, got {timestamp!r}", from_cli)

    return timestamp


def valid_start_timestamp(start_time: str, from_cli: bool = False) -> str:
    timestamp = valid_timestamp(start_time, from_cli)
    timestamp_as_seconds = U.timestamp_to_seconds(timestamp)
    timestamp_as_seconds = (
        non_negative_float(timestamp, from_cli)
        if timestamp_as_seconds is None
        else non_negative_float(timestamp_as_seconds, from_cli)
    )

    return timestamp


def valid_stop_timestamp(stop_time: str, from_cli: bool = False) -> str:
    timestamp = valid_timestamp(stop_time, from_cli)
    timestamp_as_seconds = U.timestamp_to_seconds(timestamp)
    timestamp_as_seconds = (
        positive_float(timestamp, from_cli)
        if timestamp_as_seconds is None
        else positive_float(timestamp_as_seconds, from_cli)
    )

    return timestamp


def valid_start_time(
    start_time: t.Union[float, str], from_cli: bool = False
) -> t.Union[float, str]:
    try:
        start_time_float = float(start_time)
    except ValueError:
        return valid_start_timestamp(str(start_time), from_cli)
    else:
        return non_negative_float(start_time_float, from_cli)


def valid_stop_time(
    stop_time: t.Union[float, str], from_cli: bool = False
) -> t.Union[float, str]:
    try:
        stop_time_float = float(stop_time)
    except ValueError:
        return valid_stop_timestamp(str(stop_time), from_cli)
    else:
        return positive_float(stop_time_float, from_cli)


def valid_extraction_range(
    start_second: float, stop_second: float, video_length_second: float
) -> bool:
    if start_second > video_length_second:
        _raise_error(
            f"start second ({start_second}) exceeds "
            f"length of video {video_length_second}"
        )

    if start_second == stop_second:
        _raise_error(
            f"start second ({start_second}) equals stop second ({stop_second})"
        )

    if start_second > stop_second:
        _raise_error(
            f"start second ({start_second}) exceeds stop second ({stop_second})"
        )

    return True


def valid_capture_rate(capture_rate: int, start_frame: int, stop_frame: int) -> int:
    if capture_rate > (stop_frame - start_frame):
        _raise_error(
            f"capture rate ({capture_rate}) exceeds range between "
            f"start ({start_frame}) and stop ({stop_frame}) frames"
        )

    return capture_rate


def valid_resize_value(
    resize_value: t.Union[float, str], from_cli: bool = False
) -> float:
    """Resize has an arbitrary max value of 7680, which is used to prevent
    the user from accidentally resizing output to abnormally large size.
    """
    try:
        val = float(resize_value)
    except ValueError:
        _raise_error(f"invalid resize value, got {resize_value!r}", from_cli)

    if not 0.01 <= val <= 7680:
        _raise_error(
            f"resize value must be between 0.01 and 7680, got {resize_value}", from_cli
        )

    return val


def valid_dimensions(dimensions: t.Tuple[int, int]) -> t.Tuple[int, int]:
    if len(dimensions) != 2:
        _raise_error(f"invalid dimensions, got {dimensions!r}")

    dims = tuple([positive_int(dim) for dim in list(dimensions)])
    return t.cast(t.Tuple[int, int], dims)


def valid_rotate_value(rotate_value: t.Union[int, str], from_cli: bool = False) -> int:
    """Valid rotate values are 0, 90, 180, 270."""
    try:
        val = int(rotate_value)
    except ValueError:
        _raise_error(
            f"invalid rotate value, got {rotate_value!r}\n"
            f"valid rotate values: {C.VALID_ROTATE_VALUES}",
            from_cli,
        )

    if val not in C.VALID_ROTATE_VALUES:
        _raise_error(
            f"rotate value entered not a valid rotate value, got {rotate_value}\n"
            f"valid rotate values: {C.VALID_ROTATE_VALUES}",
            from_cli,
        )

    return val


def valid_audio_format(audio_format: str, from_cli: bool = False) -> str:
    audio_format = audio_format.lower().strip(".")
    if audio_format not in C.VALID_AUDIO_FORMATS:
        _raise_error(
            f"invalid audio format, got {audio_format!r}\n"
            f"valid audio formats: {C.VALID_AUDIO_FORMATS}",
            from_cli,
        )

    return audio_format


def valid_image_format(image_format: str, from_cli: bool = False) -> str:
    image_format = image_format.lower().strip(".")
    if image_format not in C.VALID_IMAGE_FORMATS:
        _raise_error(
            f"invalid image format, got {image_format!r}\n"
            f"valid image formats: {C.VALID_IMAGE_FORMATS}",
            from_cli,
        )

    return image_format


def positive_int_cli(num: str) -> int:
    return positive_int(num, from_cli=True)


def positive_float_cli(num: str) -> float:
    return positive_float(num, from_cli=True)


def non_negative_float_cli(num: str) -> float:
    return non_negative_float(num, from_cli=True)


def valid_dir_cli(dir: str) -> Path:
    return valid_dir(dir, from_cli=True)


def valid_filepath_cli(filepath: str) -> Path:
    return valid_filepath(filepath, from_cli=True)


def valid_filename_cli(filename: str) -> str:
    return valid_filename(filename, from_cli=True)


def valid_audio_format_cli(audio_format: str) -> str:
    return valid_audio_format(audio_format, from_cli=True)


def valid_image_format_cli(image_format: str) -> str:
    return valid_image_format(image_format, from_cli=True)


def valid_resize_value_cli(resize_value: str) -> float:
    return valid_resize_value(resize_value, from_cli=True)


def valid_rotate_value_cli(rotate_value: str) -> int:
    return valid_rotate_value(rotate_value, from_cli=True)


def valid_start_time_cli(start_time: str) -> t.Union[float, str]:
    return valid_start_time(start_time, from_cli=True)


def valid_stop_time_cli(stop_time: str) -> t.Union[float, str]:
    return valid_stop_time(stop_time, from_cli=True)
