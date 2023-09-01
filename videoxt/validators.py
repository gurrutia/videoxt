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
    except (ValueError, TypeError):
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
    except (ValueError, TypeError):
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
    except (ValueError, TypeError):
        _raise_error(f"expected numeric value, got {num!r}", from_cli)

    if value < 0:
        _raise_error(f"expected non-negative number, got {num}", from_cli)

    return value


def valid_dir(dir: t.Union[Path, str], from_cli: bool = False) -> Path:
    """Validates a directory as a Path or str exists and returns a Path object if valid."""
    if dir is None:
        _raise_error(f"invalid directory, got {dir!r}", from_cli)

    dir_path = Path(dir)

    if not dir_path.is_dir():
        _raise_error(f"directory not found, got {dir_path!r}", from_cli)

    return dir_path


def valid_filepath(filepath: t.Union[Path, str], from_cli: bool = False) -> Path:
    """Validates a file exists as a Path or str and returns a Path object if valid."""
    if filepath is None:
        _raise_error(f"invalid filepath, got {filepath!r}", from_cli)

    filepath_path = Path(filepath)

    if not filepath_path.is_file():
        _raise_error(f"file not found, got {filepath_path}", from_cli)

    return filepath_path


def valid_filename(filename: str, from_cli: bool = False) -> str:
    """Validates filenames are valid and returns the input filename if valid."""
    if filename is None:
        _raise_error(f"invalid filename, got {filename!r}", from_cli)

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
    """Verifies that a timestamp, typically used for video playback on
    streaming services, adheres to accepted formats. Microseconds are truncated.

    Accepted:  `M:SS`, `MM:SS`, `H:MM:SS`, `HH:MM:SS`
    Unaccepted: `S`, `H:M:S`, values greater than 59
    """
    if timestamp is None or not timestamp:
        _raise_error(f"invalid timestamp, got {timestamp!r}", from_cli)

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


def valid_extraction_range(start: float, stop: float, duration: float) -> bool:
    """Validates the extraction range and ensures it is within valid bounds.

    - start second must be less than the duration of the video
    - start second must be less than the stop second

    Args:
    -----
        start (float): Start second of the extraction range.
        stop (float): Stop second of the extraction range.
        duration (float): Length of the video in seconds.

    Returns:
    --------
        bool: True if the extraction range is valid.

    Raises:
    -------
        ValidationException: If the extraction range is invalid.
    """
    if start > duration:
        _raise_error(f"Start second ({start}) exceeds video length ({duration})")

    if start >= stop:
        _raise_error(f"Start second ({start}) must be before stop second ({stop})")

    return True


def valid_capture_rate(capture_rate: int, first_frame: int, last_frame: int) -> int:
    """Validates that the capture rate is a positive integer less than or equal to the
    difference between the first and last frames. Returns the capture rate if valid,
    otherwise raises an error.

    Args:
    -----
        capture_rate (int): The capture rate to validate.
        first_frame (int): The first frame of the extraction range.
        last_frame (int): The last frame of the extraction range.

    Returns:
    --------
        int: The capture rate if valid.

    Raises:
    -------
        ValidationException: If the capture rate is not a positive integer or exceeds
            the range between the first and last frames.
    """
    if capture_rate < 1:
        raise ValidationException(
            f"capture rate must be a positive integer: {capture_rate}"
        )

    if capture_rate > (last_frame - first_frame):
        raise ValidationException(
            f"capture rate ({capture_rate}) exceeds range between "
            f"first frame ({first_frame}) and last frame ({last_frame})"
        )

    return capture_rate


def valid_resize_value(
    resize_value: t.Union[float, str], from_cli: bool = False
) -> float:
    """Validates that the resize value, a number, or a string representing a
    number, is greater than 0. The resize value represents the percentage of
    the original video dimensions to resize the output media to.

    For example, a resize value of 0.5 will resize the media to 50% of its
    original dimensions. A resize value of 2.0 will resize the media to 200%
    of its original dimensions.

    Args:
    -----
        resize_value (Union[float, str]): The resize value to validate.
        from_cli (bool, optional): If True, raise an argparse error. Otherwise,
            raise a ValidationException. Defaults to False.

    Returns:
    --------
        float: The resize value if valid.

    Raises:
    -------
        argparse.ArgumentTypeError: If from_cli is True and the resize value is invalid.
        ValidationException: If from_cli is False and the resize value is invalid.
    """
    try:
        value = float(resize_value)
    except (TypeError, ValueError):
        _raise_error(f"resize value must be a number, got {resize_value!r}", from_cli)

    if value <= 0:
        _raise_error(
            f"resize value must be greater that 0, got {resize_value}", from_cli
        )

    return value


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
    if audio_format not in C.SUPPORTED_AUDIO_FORMATS:
        _raise_error(
            f"invalid audio format, got {audio_format!r}\n"
            f"supported audio formats: {C.SUPPORTED_AUDIO_FORMATS}",
            from_cli,
        )

    return audio_format


def valid_image_format(image_format: str, from_cli: bool = False) -> str:
    """Validates the image format is valid and returns the format if valid. An invalid
    image format is one that is not in the list of valid image formats located in
    `constants.py`.

    Supported formats: `bmp`, `dib`, `jp2`, `jpeg`, `jpg`, `png`, `tif`, `tiff`, `webp`
    """
    image_format = image_format.lower().strip(".")
    if image_format not in C.SUPPORTED_IMAGE_FORMATS:
        _raise_error(
            f"invalid image format, got {image_format!r}\n"
            f"supported image formats: {C.SUPPORTED_IMAGE_FORMATS}",
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

    if video_format not in C.SUPPORTED_VIDEO_FORMATS:
        _raise_error(
            f"invalid video format, got {video_format!r}\n"
            f"supported video formats: {C.SUPPORTED_VIDEO_FORMATS}",
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
