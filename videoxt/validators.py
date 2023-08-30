"""User input validators called from Request objects and command line."""
import argparse
import re
import typing as t
from pathlib import Path

import videoxt.constants as C
import videoxt.utils as U
from videoxt.exceptions import ValidationException


def _raise_error(error_msg: str, from_cli: bool = False) -> None:
    """Raise an error message. If `from_cli` is `True`, raise an argparse error.
    Otherwise, raise a ValidationException.
    """
    if from_cli:
        raise argparse.ArgumentTypeError(error_msg)
    raise ValidationException(error_msg)


def positive_int(num: t.Union[float, int, str], from_cli: bool = False) -> int:
    """Validates floats, integers or strings are positive integers and returns
    an integer if valid.
    """
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
    """Validates floats, integers or strings are positive floats and returns a float if valid."""
    try:
        value = float(num)
    except (ValueError, TypeError):
        _raise_error(f"expected numeric value, got {num!r}", from_cli)

    if value <= 0:
        _raise_error(f"expected positive number, got {num}", from_cli)

    return value


def non_negative_int(num: t.Union[float, int, str], from_cli: bool = False) -> int:
    """Validates floats, integers or strings are non-negative integers and returns
    an integer if valid.
    """
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
    """Validates floats, integers or strings are non-negative floats and returns a float
    if valid.
    """
    try:
        value = float(num)
    except ValueError:
        _raise_error(f"expected numeric value, got {num!r}", from_cli)

    if value < 0:
        _raise_error(f"expected non-negative number, got {num}", from_cli)

    return value


def valid_dir(dir: t.Union[Path, str], from_cli: bool = False) -> Path:
    """Validates a directory as a Path or str exists and returns a Path object if valid."""
    dir_path = Path(dir)

    if not dir_path.is_dir():
        _raise_error(f"directory not found, got {dir_path!r}", from_cli)

    return dir_path


def valid_filepath(filepath: t.Union[Path, str], from_cli: bool = False) -> Path:
    """Validates a file exists as a Path or str and returns a Path object if valid."""
    filepath_path = Path(filepath)

    if not filepath_path.is_file():
        _raise_error(f"file not found, got {filepath_path}", from_cli)

    return filepath_path


def valid_filename(filename: str, from_cli: bool = False) -> str:
    """Validates filenames are valid and returns the input filename if valid."""
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
    """Validates timestamps are in the correct format. Microseconds are truncated.

    Correct formats: `HH:MM:SS`, `H:MM:SS`, `MM:SS`, `M:SS`
    """
    timestamp = timestamp.split(".")[0]

    regex = r"^([0-9]|[0-5][0-9])(:[0-5][0-9]){1,2}$"
    if not bool(re.match(regex, timestamp)):
        _raise_error(f"invalid timestamp, got {timestamp!r}", from_cli)

    return timestamp


def valid_start_timestamp(start_time: str, from_cli: bool = False) -> str:
    """Validates start timestamps are in the correct format, if so, converts to seconds
    and validates the timestamp is non-negative and returns the timestamp string if valid
    """
    timestamp = valid_timestamp(start_time, from_cli)
    timestamp_as_seconds = U.timestamp_to_seconds(timestamp)
    timestamp_as_seconds = (
        non_negative_float(timestamp, from_cli)
        if timestamp_as_seconds is None
        else non_negative_float(timestamp_as_seconds, from_cli)
    )

    return timestamp


def valid_stop_timestamp(stop_time: str, from_cli: bool = False) -> str:
    """Validates stop timestamps are in the correct format, if so, converts to seconds
    and validates the timestamp is positive and returns the timestamp string if valid
    """
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
    """Validates start times are in the correct format and not negative. Returns the
    start time as a float if valid or a string if the start time is a timestamp.
    """
    try:
        start_time_float = float(start_time)
    except ValueError:
        return valid_start_timestamp(str(start_time), from_cli)
    else:
        return non_negative_float(start_time_float, from_cli)


def valid_stop_time(
    stop_time: t.Union[float, str], from_cli: bool = False
) -> t.Union[float, str]:
    """Validates stop times are in the correct format and not negative. Returns the
    stop time as a float if valid or a string if the stop time is a timestamp."""
    try:
        stop_time_float = float(stop_time)
    except ValueError:
        return valid_stop_timestamp(str(stop_time), from_cli)
    else:
        return positive_float(stop_time_float, from_cli)


def valid_extraction_range(
    start_second: float, stop_second: float, video_length_second: float
) -> bool:
    """Validates the extraction range is valid and returns True if valid."""
    if start_second > video_length_second:
        _raise_error(
            f"start second ({start_second}) exceeds "
            f"length of video in seconds ({video_length_second})"
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
    """Validates the capture rate is valid and returns the capture rate if valid. An
    invalid capture rate is one that exceeds the range between the start and stop
    frames. For example: if the start frame is 0 and the stop frame is 10, the
    capture rate can't be greater than 10.
    """
    if capture_rate > (stop_frame - start_frame):
        _raise_error(
            f"capture rate ({capture_rate}) exceeds range between "
            f"start ({start_frame}) and stop ({stop_frame}) frames"
        )

    return capture_rate


def valid_resize_value(
    resize_value: t.Union[float, str], from_cli: bool = False
) -> float:
    """Validates the resize value is valid and returns the value as a float if valid.
    Resize has an arbitrary max value of 7680, which is used to prevent the user from
    accidentally resizing output to abnormally large size.
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
    """Validates the dimensions are valid and returns the dimensions as a tuple of
    ints if valid.
    """
    if len(dimensions) != 2:
        _raise_error(f"invalid dimensions, got {dimensions!r}")

    dims = tuple([positive_int(dim) for dim in list(dimensions)])
    return t.cast(t.Tuple[int, int], dims)


def valid_rotate_value(rotate_value: t.Union[int, str], from_cli: bool = False) -> int:
    """Validates the rotate value is valid and returns the value as an int if valid.

    Valid rotate values are `0`, `90`, `180`, `270`.
    """
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
    """Validates the audio format is valid and returns the format if valid. An invalid
    audio format is one that is not in the list of valid audio formats located in
    `constants.py`.

    Valid audio formats: `m4a`, `mp3`, `ogg`, `wav`
    """
    audio_format = audio_format.lower().strip(".")
    if audio_format not in C.VALID_AUDIO_FORMATS:
        _raise_error(
            f"invalid audio format, got {audio_format!r}\n"
            f"valid audio formats: {C.VALID_AUDIO_FORMATS}",
            from_cli,
        )

    return audio_format


def valid_image_format(image_format: str, from_cli: bool = False) -> str:
    """Validates the image format is valid and returns the format if valid. An invalid
    image format is one that is not in the list of valid image formats located in
    `constants.py`.

    Valid image formats: `bmp`, `dib`, `jpeg`, `jpg`, `png`, `tiff`, `tif`, `webp`
    """
    image_format = image_format.lower().strip(".")
    if image_format not in C.VALID_IMAGE_FORMATS:
        _raise_error(
            f"invalid image format, got {image_format!r}\n"
            f"valid image formats: {C.VALID_IMAGE_FORMATS}",
            from_cli,
        )

    return image_format


def valid_video_filepath(video_filepath: Path, from_cli: bool = False) -> Path:
    """Returns the filepath to the video file if the file extension is a valid
    video format as defined in `constants.py`.

    Args:
    -----
    video_filepath : Path
        Filepath to the presumed video file.
    from_cli : bool
        If True, raise an argparse error. Otherwise, raise a ValidationException.

    Returns:
    --------
    Path : The filepath to the video file if valid.

    Raises:
    -------
    argparse.ArgumentTypeError : If from_cli is True and the video format is invalid.
    ValidationException : If from_cli is False and the video format is invalid.
    """
    video_filepath = valid_filepath(video_filepath, from_cli)
    video_format = video_filepath.name.split(".")[-1].lower()

    if video_format not in C.VALID_VIDEO_FORMATS:
        _raise_error(
            f"invalid video format, got {video_format!r}\n"
            f"supported video formats: {C.VALID_VIDEO_FORMATS}",
            from_cli,
        )

    return video_filepath


def positive_int_cli(num: str) -> int:
    """cli version of `positive_int`"""
    return positive_int(num, from_cli=True)


def positive_float_cli(num: str) -> float:
    """cli version of `positive_float`"""
    return positive_float(num, from_cli=True)


def non_negative_float_cli(num: str) -> float:
    """cli version of `non_negative_float`"""
    return non_negative_float(num, from_cli=True)


def valid_dir_cli(dir: str) -> Path:
    """cli version of `valid_dir`"""
    return valid_dir(dir, from_cli=True)


def valid_filepath_cli(filepath: str) -> Path:
    """cli version of `valid_filepath`"""
    return valid_filepath(filepath, from_cli=True)


def valid_filename_cli(filename: str) -> str:
    """cli version of `valid_filename`"""
    return valid_filename(filename, from_cli=True)


def valid_audio_format_cli(audio_format: str) -> str:
    """cli version of `valid_audio_format`"""
    return valid_audio_format(audio_format, from_cli=True)


def valid_image_format_cli(image_format: str) -> str:
    """cli version of `valid_image_format`"""
    return valid_image_format(image_format, from_cli=True)


def valid_resize_value_cli(resize_value: str) -> float:
    """cli version of `valid_resize_value`"""
    return valid_resize_value(resize_value, from_cli=True)


def valid_rotate_value_cli(rotate_value: str) -> int:
    """cli version of `valid_rotate_value`"""
    return valid_rotate_value(rotate_value, from_cli=True)


def valid_start_time_cli(start_time: str) -> t.Union[float, str]:
    """cli version of `valid_start_time`"""
    return valid_start_time(start_time, from_cli=True)


def valid_stop_time_cli(stop_time: str) -> t.Union[float, str]:
    """cli version of `valid_stop_time`"""
    return valid_stop_time(stop_time, from_cli=True)
