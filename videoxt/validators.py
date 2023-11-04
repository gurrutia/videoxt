"""Contains functions to validate user input and other data."""
import re
from pathlib import Path
from typing import cast

import videoxt.constants as C
import videoxt.utils as U
from videoxt.exceptions import ValidationError


def positive_int(n: float | int | str) -> int:
    """
    Return a positive integer from a float, integer or string.

    Args:
    -----
        `n` (float | int | str): The number to validate.

    Returns:
    -----
        `int`: The number as an integer if positive.

    Raises:
    -----
        `ValidationError`: If the number is not a positive integer.
    """
    try:
        value = float(n)
    except (ValueError, TypeError):
        raise ValidationError(f"Expected integer, got {n!r}")

    if not value.is_integer():
        raise ValidationError(f"Expected integer, got {n}")

    if value <= 0:
        raise ValidationError(f"Expected positive integer, got {n}")

    return int(value)


def positive_float(n: float | int | str) -> float:
    """
    Return a positive float from a float, integer or string.

    Args:
    -----
        `n` (float | int | str): The number to validate.

    Returns:
    -----
        `float`: The number as a float if positive.

    Raises:
    -----
        `ValidationError`: If the number is not a positive float.
    """
    try:
        value = float(n)
    except (ValueError, TypeError):
        raise ValidationError(f"Expected numeric value, got {n!r}")

    if value <= 0:
        raise ValidationError(f"Expected positive number, got {n}")

    return value


def non_negative_int(n: float | int | str) -> int:
    """
    Return a non-negative integer from a float, integer or string.

    Args:
    -----
        `n` (float | int | str): The number to validate.

    Returns:
    -----
        `int`: The number as an integer if non-negative.

    Raises:
    -----
        `ValidationError`: If the number is not a non-negative integer.
    """
    try:
        value = float(n)
    except (ValueError, TypeError):
        raise ValidationError(f"Expected integer, got {n!r}")

    if not value.is_integer():
        raise ValidationError(f"Expected integer, got {n!r}")

    if value < 0:
        raise ValidationError(f"Expected non-negative integer, got {n}")

    return int(value)


def non_negative_float(n: float | int | str) -> float:
    """
    Return a non-negative float from a float, integer or string.

    Args:
    -----
        `n` (float | int | str): The number to validate.

    Returns:
    -----
        `float`: The number as a float if non-negative.

    Raises:
    -----
        `ValidationError`: If the number is not a non-negative float.
    """
    try:
        value = float(n)
    except (ValueError, TypeError):
        raise ValidationError(f"Expected numeric value, got {n!r}")

    if value < 0:
        raise ValidationError(f"Expected non-negative number, got {n}")

    return value


def valid_dir(directory: Path | str) -> Path:
    """
    Validate a path is a directory and exists and return it.

    Args:
    -----
        `directory` (Path | str): The directory to validate.

    Returns:
    -----
        `Path`: The directory as a Path object if valid.

    Raises:
    -----
        `ValidationError`: If the path is not a directory or does not exist.
    """
    if directory is None:
        raise ValidationError(f"Directory cannot be None, got {directory!r}")

    dir_path = Path(directory)

    if not dir_path.is_dir():
        raise ValidationError(f"Directory not found, got {directory!r}")

    if dir_path == Path("/"):
        raise ValidationError(f"Invalid directory, got {directory!r}")

    if dir_path == Path("."):
        dir_path = Path.cwd()

    if dir_path == Path(".."):
        dir_path = Path.cwd().parent

    return dir_path


def valid_filepath(filepath: Path | str, is_video: bool = False) -> Path:
    """
    Validate a path is a file and exists and return it.

    Args:
    -----
        `filepath` (Path | str):
            The filepath to validate.
        `is_video` (bool) :
            If True, the filepath is checked against a set of supported video file
            suffixes.

    Returns:
    -----
        `Path`: The filepath as a Path object if it is a file and exists.

    Raises:
    -----
        `ValidationError`: If the path is not a file or does not exist.
    """
    if filepath is None:
        raise ValidationError(f"Filepath cannot be None, got {filepath!r}")

    try:
        fp = Path(filepath)
    except TypeError:
        raise ValidationError(f"Invalid filepath, got {filepath!r}")

    if not fp.exists():
        raise ValidationError(f"File not found, got {filepath!r}")

    if not fp.is_file():
        raise ValidationError(f"Filepath provided is not a file, got {filepath!r}")

    if is_video:
        valid_video_file_suffix(fp.suffix)

    return fp


def valid_filename(filename: str) -> str:
    """
    Validate a filename does not contain invalid characters and return it.

    In the context of `videoxt`, a filename refers to a Path().stem.

    Args:
    -----
        `filename` (str): The filename to validate.

    Returns:
    -----
        `str`: The filename if it does not contain invalid characters.

    Raises:
    -----
        `ValidationError`: If the filename is None, empty or contains invalid chars.
    """
    if filename is None:
        raise ValidationError(f"Invalid filename, got {filename!r}")

    if not filename:
        raise ValidationError(f"Invalid filename, got {filename!r}")

    invalid_chars = r"[\\/:*?\"<>|]"
    if re.search(invalid_chars, filename):
        raise ValidationError(
            f"Invalid filename, got {filename!r}\n"
            f"filename can't contain any of the following characters: \\/:*?\"<>|"
        )

    return filename


def valid_timestamp(timestamp: str) -> str:
    """
    Validate a timestamp is in the correct format and return it if valid.

    In the context of `videoxt` a timestamp is one typically seen during playback on
    video sharing or streaming platforms. Microseconds are truncated.

    Valid:  `M:SS`, `MM:SS`, `H:MM:SS`, `HH:MM:SS`.
    Invalid: `S`, `SS`, `H:M:S`, values greater than 59 for hours, minutes or seconds.

    Args:
    -----
        `timestamp` (str): The timestamp to validate.

    Returns:
    -----
        `str`: The timestamp if valid.

    Raises:
    -----
        `ValidationError`:
            If the timestamp is None, empty, or does not match the regex pattern.
    """
    if timestamp is None or not timestamp:
        raise ValidationError(f"Timestamp string is empty or None, got {timestamp!r}")

    timestamp = timestamp.split(".")[0]

    regex = r"^([0-9]|[0-5][0-9])(:[0-5][0-9]){1,2}$"
    if not bool(re.match(regex, timestamp)):
        raise ValidationError(
            f"Invalid timestamp format, got {timestamp!r}\n"
            f"Allowed: 'M:SS', 'MM:SS', 'H:MM:SS', 'HH:MM:SS'"
        )

    return timestamp


def valid_start_timestamp(start_timestamp: str) -> str:
    """
    Validate a start timestamp is in the correct format and return it if valid.

    Valid:  `M:SS`, `MM:SS`, `H:MM:SS`, `HH:MM:SS`.
    Invalid: `S`, `SS`, `H:M:S`, values greater than 59 for hours, minutes or seconds.

    See `valid_timestamp` for more information on how timestamps are validated.

    Args:
    -----
        `start_timestamp` (str) : The timestamp to validate (Ex: '12:34').

    Returns:
    -----
        `str`: The timestamp as a string if valid.
    """
    timestamp = valid_timestamp(start_timestamp)
    timestamp_as_seconds = U.timestamp_to_seconds(timestamp)
    timestamp_as_seconds = (
        non_negative_float(timestamp)
        if timestamp_as_seconds is None
        else non_negative_float(timestamp_as_seconds)
    )

    return timestamp


def valid_stop_timestamp(stop_timestamp: str) -> str:
    """
    Validate a stop timestamp is in the correct format and return it if valid.

    Valid:  `M:SS`, `MM:SS`, `H:MM:SS`, `HH:MM:SS`.
    Invalid: `S`, `SS`, `H:M:S`, values greater than 59 for hours, minutes or seconds.

    See `valid_timestamp` for more information on how timestamps are validated.

    Args:
    -----
        `stop_timestamp` (str): The timestamp to validate (Ex: '12:34').

    Returns:
    -----
        `str`: The timestamp as a string if valid.
    """
    timestamp = valid_timestamp(stop_timestamp)
    timestamp_as_seconds = U.timestamp_to_seconds(timestamp)
    timestamp_as_seconds = (
        positive_float(timestamp)
        if timestamp_as_seconds is None
        else positive_float(timestamp_as_seconds)
    )

    return timestamp


def valid_start_time(start_time: float | int | str) -> float | str:
    """
    Validate any start time provided is in the correct format and not negative.

    Args:
    -----
        `start_time` (float | int | str): The start time to validate.

    Returns:
    -----
        `float | str`: The start time as a float or string if valid.

    Raises:
    -----
        `ValidationError`:
            If start time is not a non-negative float or a properly formatted timestamp.
    """
    try:
        start_time_float = float(start_time)
    except ValueError:
        try:
            return valid_start_timestamp(str(start_time))
        except ValidationError:
            raise ValidationError(
                f"Invalid start time, got {start_time!r}\n"
                "Start time must be a non-negative number or a properly formatted "
                "timestamp (Ex: 'HH:MM:SS')."
            )
    else:
        try:
            return non_negative_float(start_time_float)
        except ValidationError:
            raise ValidationError(
                f"Invalid start time, got {start_time!r}\n"
                "Start time must be a non-negative number or a properly formatted "
                "timestamp (Ex: 'HH:MM:SS')."
            )


def valid_stop_time(stop_time: float | int | str) -> float | str:
    """
    Validate any stop time provided is in the correct format and not negative.

    Args:
    -----
        `stop_time` (float | int | str): The stop time to validate.

    Returns:
    -----
        `float | str`: The stop time as a float or string if valid.

    Raises:
    -----
        `ValidationError`:
            If stop time is not a positive float or a properly formatted timestamp.
    """
    try:
        stop_time_float = float(stop_time)
    except ValueError:
        try:
            return valid_stop_timestamp(str(stop_time))
        except ValidationError:
            raise ValidationError(
                f"Invalid stop time, got {stop_time!r}\n"
                "Stop time must be a positive number or a properly formatted "
                "timestamp (Ex: 'HH:MM:SS')."
            )
    else:
        try:
            return positive_float(stop_time_float)
        except ValidationError:
            raise ValidationError(
                f"Invalid stop time, got {stop_time!r}\n"
                "Stop time must be a positive number or a properly formatted "
                "timestamp (Ex: 'HH:MM:SS')."
            )


def valid_extraction_range(
    start: float, stop: float, duration: float
) -> tuple[float, float, float]:
    """
    Validate the extraction range is within bounds and return it.

    Args:
    -----
        `start` (float):
            Extraction start second.
        `stop` (float):
            Extraction stop second.
        `duration` (float):
            Duration of the video in seconds.

    Returns:
    -----
        `Tuple[float, float, float]`:
            The start, stop and duration if valid (start, stop, duration).

    Raises:
    -----
        `ValidationError`:
        - If the start second is greater than or equal to the duration.
        - If the stop second is less than or equal to the start second.
    """
    if stop > duration:
        stop = duration

    if start < 0:
        start = 0

    if start >= duration:
        raise ValidationError(
            f"Start second ({start}) is >= video duration ({duration})"
        )

    if stop <= start:
        raise ValidationError(
            f"Stop second ({stop}) must be greater than start second ({start})"
        )

    return start, stop, duration


def valid_dimensions(dimensions: tuple[int, int]) -> tuple[int, int]:
    """
    Validate values in a dimensions tuple are positive integers and return it.

    Args:
    -----
        `dimensions` (tuple[int, int]): The dimensions to validate.

    Returns:
    -----
        `tuple[int, int]`: The dimensions if both integers are positive.

    Raises:
    -----
        `ValidationError`:
            If the length of the tuple isn't 2 or one or more of the values are not
            positive integers
    """
    if len(dimensions) != 2:
        raise ValidationError(f"Invalid dimensions, got {dimensions!r}")

    dims = tuple([positive_int(dim) for dim in list(dimensions)])

    return cast(tuple[int, int], dims)


def valid_rotate_value(n: float | int | str) -> int:
    """
    Validate a rotate value is either 0, 90, 180 or 270.

    Args:
    -----
        `n` (float | int | str): The rotate value to validate.

    Returns:
    -----
        `int`: The rotate value if 0, 90, 180, or 270.

    Raises:
    -----
        `ValidationError`: If the rotate value is invalid.
    """
    try:
        val = int(n)
    except ValueError:
        raise ValidationError(
            f"Invalid rotate value, got {n!r}\n"
            f"Allowed values: {C.VALID_ROTATE_VALUES}"
        )

    if val not in C.VALID_ROTATE_VALUES:
        raise ValidationError(
            f"Invalid rotate value, got {n}\n"
            f"Allowed values: {C.VALID_ROTATE_VALUES}"
        )

    return val


def valid_audio_format(audio_format: str) -> str:
    """
    Validate audio format is supported by `videoxt` and return it if so.

    Input is converted to lowercase and stripped of any leading periods. `Mp3` and
    `.MP3` would both be considered valid and returned as `mp3`.

    See supported formats here: `videoxt.constants.SUPPORTED_AUDIO_FORMATS`.

    Args:
    -----
        `audio_format` (str): The audio format to validate.

    Returns:
    -----
        `str`: The audio format if supported.

    Raises:
    -----
        `ValidationError`: If the audio format is not supported.
    """
    fmt = audio_format.lower().lstrip(".")
    if fmt not in C.SUPPORTED_AUDIO_FORMATS:
        raise ValidationError(
            f"Unsupported audio format, got {audio_format!r}\n"
            f"Supported formats: {C.SUPPORTED_AUDIO_FORMATS}"
        )

    return fmt


def valid_image_format(image_format: str) -> str:
    """
    Validate image format is supported by `videoxt` and return it if so.

    Input is converted to lowercase and stripped of any leading periods. `jpG` and
    `.JPG` would both be considered valid and returned as `jpg`.

    See supported formats here: `videoxt.constants.SUPPORTED_IMAGE_FORMATS`.

    Args:
    -----
        `image_format` (str): The image format to validate.

    Returns:
    -----
        `str`: The image format if valid.

    Raises:
    -----
        `ValidationError`: If the image format is not supported.
    """
    fmt = image_format.lower().lstrip(".")
    if fmt not in C.SUPPORTED_IMAGE_FORMATS:
        raise ValidationError(
            f"Invalid image format, got {image_format!r}\n"
            f"Supported image formats: {C.SUPPORTED_IMAGE_FORMATS}"
        )

    return fmt


def valid_volume(volume: float | int | str) -> float:
    """
    Validate and return non-negative float audio volume. If input is negative, set to 0.

    Args:
    -----
        `volume` (float | int | str): The volume to validate.

    Returns:
    -----
        `float`: The volume as a float if valid.

    Raises:
    -----
        `ValidationError`: If the volume is None.
    """
    if volume is None:
        raise ValidationError("Volume cannot be None.")

    if isinstance(volume, (float, int)):
        return volume if volume > 0 else 0

    try:
        vol = float(volume)
    except (ValueError, TypeError):
        raise ValidationError(f"Volume expects numeric value, got {volume!r}")

    return vol if vol > 0 else 0


def valid_video_file_suffix(suffix: str) -> str:
    """
    Validate suffix provided is supported by `videoxt` and return it.

    Input is converted to lowercase and stripped of any leading periods. `Mp4` and
    `.MP4` would both be considered valid and returned as `mp4`.

    Args:
    -----
        `suffix` (str): The suffix to validate.

    Returns:
    -----
        `str`: The suffix if valid.

    Raises:
    -----
        `ValidationError`: If the video format is not supported.
    """
    sfx = suffix.lower().lstrip(".")
    if sfx not in C.SUPPORTED_VIDEO_FORMATS:
        raise ValidationError(
            f"Invalid video file suffix, got {suffix!r}\n"
            f"Supported: {C.SUPPORTED_VIDEO_FORMATS}"
        )

    return sfx


def valid_fps(fps: float | int | str) -> float:
    """
    Validate and return a positive float fps.

    Args:
    -----
        `fps` (float | int | str): The fps to validate.

    Returns:
    -----
        `float`: The fps as a float if valid.

    Raises:
    -----
        `ValidationError`: If the fps is None or not a positive float.
    """
    if fps is None:
        raise ValidationError("FPS cannot be None.")

    try:
        return positive_float(fps)
    except ValidationError:
        raise ValidationError(
            f"Invalid fps, got {fps!r}\nFPS must be a positive number."
        )


def valid_dimensions_str(dimensions: str) -> tuple[int, int]:
    """
    Validate and return a tuple of positive integers from a string of dimensions.

    Args:
    -----
        `dimensions` (str): The dimensions to validate.

    Returns:
    -----
        `tuple[int, int]`: The dimensions as a tuple of integers if valid.

    Raises:
    -----
        `ValidationError`: If the dimensions are None, empty, or not in this format:
            'WxH' (Ex: '1920x1080').
    """
    if not dimensions:
        raise ValidationError(
            f"Empty dimensions provided, got {dimensions!r}\n"
            "Expected format: 'WxH' (Ex: '1920x1080')"
        )

    if dimensions.count("x") > 1:
        raise ValidationError(
            f"Too many dimensions provided, got {dimensions!r}\n"
            "Expected format: 'WxH' (Ex: '1920x1080')"
        )

    try:
        dims = tuple(positive_int(dim) for dim in tuple(dimensions.split("x")))
    except ValidationError:
        raise ValidationError(
            f"Invalid dimensions, got {dimensions!r}\n"
            "Dimensions must be positive integers.\n"
            "Expected format: 'WxH' (Ex: '1920x1080')"
        )

    return cast(tuple[int, int], dims)


def valid_resize(resize: float | int | str) -> float:
    """
    Validate and return a positive float resize value.

    Args:
    -----
        `resize` (float | int | str): The resize value to validate.

    Returns:
    -----
        `float`: The resize value as a float if valid.

    Raises:
    -----
        `ValidationError`: If the resize value is None or not a positive float.
    """
    if resize is None:
        raise ValidationError("Resize value cannot be None.")

    try:
        return positive_float(resize)
    except ValidationError:
        raise ValidationError(
            f"Invalid resize value, got {resize!r}\n"
            "Resize value must be a positive number."
        )


def valid_speed(speed: float | int | str) -> float:
    """
    Validate and return a positive float speed value.

    Args:
    -----
        `speed` (float | int | str): The speed value to validate.

    Returns:
    -----
        `float`: The speed value as a float if valid.

    Raises:
    -----
        `ValidationError`: If the speed value is None or not a positive float.
    """
    if speed is None:
        raise ValidationError("Speed value cannot be None.")

    try:
        return positive_float(speed)
    except ValidationError:
        raise ValidationError(
            f"Invalid speed value, got {speed!r}\n"
            "Speed value must be a positive number."
        )


def valid_capture_rate(capture_rate: float | int | str) -> int:
    """
    Validate and return a positive integer capture rate.

    Args:
    -----
        `capture_rate` (float | int | str): The capture rate to validate.

    Returns:
    -----
        `int`: The capture rate as an integer if valid.

    Raises:
    -----
        `ValidationError`: If the capture rate is None or not a positive integer.
    """
    if capture_rate is None:
        raise ValidationError("Capture rate cannot be None.")

    try:
        return positive_int(capture_rate)
    except ValidationError:
        raise ValidationError(
            f"Invalid capture rate, got {capture_rate!r}\n"
            "Capture rate must be a positive integer."
        )
