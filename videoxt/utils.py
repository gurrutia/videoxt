"""Utility functions and classes used throughout the library."""
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any, ClassVar, Protocol

from rich import print

from videoxt.constants import ExtractionMethod
from videoxt.validators import positive_float, positive_int, valid_filename


def timestamp_to_seconds(timestamp: str) -> float:
    """
    Convert a timestamp string to the total number of seconds (float) it represents.

    Accepts the formats "HH:MM:SS", "H:MM:SS", "MM:SS", "M:SS", "SS" or "S".
    Microseconds are truncated.

    Usage:
    -----
    ```python
    >>> from videoxt.utils import timestamp_to_seconds
    >>> timestamp_to_seconds("1:01")
    61.0
    >>> timestamp_to_seconds("1:01.987654321")
    61.0
    >>> timestamp_to_seconds("10:00")
    600.0
    >>> timestamp_to_seconds("1:00:00")
    3600.0
    ```

    Args:
    -----
        `timestamp` (str):
            A timestamp string in the format "HH:MM:SS", "H:MM:SS", "MM:SS", "M:SS",
            "SS" or "S"

    Returns:
    -----
        `float`: The number of seconds converted from the timestamp string.
    """
    timestamp = timestamp.split(".")[0]
    time_parts = timestamp.split(":")
    total_seconds: float = sum(
        float(part) * 60**exponent for exponent, part in enumerate(reversed(time_parts))
    )

    return total_seconds


def seconds_to_timestamp(seconds: float) -> str:
    """
    Convert seconds to a time duration string in the format "HH:MM:SS" or "H:MM:SS".

    Microseconds are truncated.

    Usage:
    -----
    ```python
    >>> from videoxt.utils import seconds_to_timestamp
    >>> seconds_to_timestamp(60)
    '0:01:00'
    >>> seconds_to_timestamp(60.987654321)
    '0:01:00'
    >>> seconds_to_timestamp(600)
    '0:10:00'
    >>> seconds_to_timestamp(3600)
    '1:00:00'
    ```

    Args:
    -----
        `seconds` (float): The number of seconds to convert to a timestamp.

    Returns:
    -----
        `str`: A timestamp string in the format "HH:MM:SS" or "H:MM:SS".
    """
    if seconds <= 0:
        return "0:00:00"

    return str(timedelta(seconds=int(seconds)))


def timedelta_to_timestamp(duration: timedelta) -> str:
    """
    Convert a timedelta to a time duration string in the format "HH:MM:SS".

    Microseconds are truncated.

    Usage:
    -----
    ```python
    >>> from videoxt.utils import timedelta_to_timestamp
    >>> timedelta_to_timestamp(timedelta(seconds=59))
    '00:00:59'
    >>> timedelta_to_timestamp(timedelta(seconds=61.987654321))
    '00:01:01'
    >>> timedelta_to_timestamp(timedelta(seconds=600))
    '00:10:00'
    ```

    Args:
    -----
        `duration` (datetime.timedelta): The duration to convert to a timestamp.

    Returns:
    -----
        `str`: A timestamp string in the format "HH:MM:SS".

    Raises:
    -----
        `ValueError`: If the duration is negative.
    """
    total_seconds = duration.total_seconds()

    if total_seconds < 0:
        raise ValueError(
            f"Invalid duration: timedelta must be non-negative: {duration}"
        )

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


def append_enumeration(index: int, tag: str | None = None) -> str:
    """
    Return an enumerated file name with the given index and optional tag.

    The returned string is intended to be appended to a file name or directory name.
    If the tag is None, only the index is used to enumerate the file name starting
    from 1. If a tag is provided, the tag is appended to the file name before the
    index. Mimics the behavior of Windows when creating a file or directory with the
    same name as an existing file or directory.

    Usage:
    -----
    ```python
    >>> from videoxt.utils import append_enumeration
    >>> append_enumeration(1)
    ' (1)'
    >>> append_enumeration(2)
    ' (2)'
    >>> append_enumeration(1, tag="_vxt")
    '_vxt'
    >>> append_enumeration(2, tag="_vxt")
    '_vxt (2)'
    ```

    Args:
    -----
        `index` (int):
            The enumeration index. Must be greater than 0.
        `tag` (str | None):
            The tag to enumerate. If None, only the index is used.

    Returns:
    -----
        `str`: The enumerated string to append to a file name or directory name.
    """
    index = 1 if index < 1 else index

    if tag is None:
        return f" ({index})"

    # Ensure the tag doesn't contain invalid characters for a file name.
    tag = valid_filename(tag)

    return f"{tag} ({index})" if index > 1 else tag


def enumerate_dir(directory: Path, tag: str | None = None) -> Path:
    """
    Return a non-existent, potentially enumerated directory path.

    See `videoxt.utils.append_enumeration` for more information on how the directory
    name is enumerated with or without a tag.

    Usage:
    -----
    ```python
    >>> from videoxt.utils import
    >>> from pathlib import Path
    >>> path = Path("test_dir")  # Assume 'test_dir' doesn't exist.
    >>> enumerate_dir(path, tag="_frames")
    Path('test_dir')
    >>> enumerate_dir(path, tag="_frames")
    Path('test_dir_frames')
    >>> enumerate_dir(path, tag="_frames")
    Path('test_dir_frames (2)')
    ```

    Args:
    -----
        `directory`:
            The path to the directory to potentially enumerate.
        `tag` (str | None):
            The tag to enumerate. If None, only the index is used.

    Returns:
    -----
        `Path`: The path to a non-existent directory.
    """
    if not directory.exists():
        return directory

    index = 1
    while True:
        append_str = append_enumeration(index, tag=tag)
        new_dir = directory.with_name(f"{directory.name}{append_str}")
        if not new_dir.exists():
            return new_dir
        index += 1


def enumerate_filepath(filepath: Path, tag: str | None = None) -> Path:
    """
    Return a non-existent, potentially enumerated file path.

    See `videoxt.utils.append_enumeration` for more information on how the file name
    is enumerated with or without a tag.

    Usage:
    -----
    ```python
    >>> from videoxt.utils import enumerate_filepath
    >>> from pathlib import Path
    >>> filepath = Path('test.mp4')  # Assume 'test.mp4' doesn't exist.
    >>> enumerate_filepath(filepath, tag="_vxt")
    Path('test.mp4')
    >>> enumerate_filepath(filepath, tag="_vxt")
    Path('test_vxt.mp4')
    >>> enumerate_filepath(filepath, tag="_vxt")
    Path('test_vxt (2).mp4')
    ```

    Args:
    -----
        `filepath` (Path): The path to the file to potentially enumerate.

    Returns:
    -----
        `Path`: The path to a non-existent file.
    """
    if not filepath.exists():
        return filepath

    index = 1
    while True:
        append_str = append_enumeration(index, tag)
        new_filename = f"{filepath.stem}{append_str}{filepath.suffix}"
        new_filepath = filepath.with_name(new_filename)

        if not new_filepath.exists():
            return new_filepath

        index += 1


def calculate_duration(frame_count: int, fps: float) -> timedelta:
    """
    Return a timedelta representing the duration of a video using frame count and fps.

    Args:
    -----
        `frame_count` (int):
            The total number of frames in the video.
        `fps` (float):
            The frames per second of the video.

    Returns:
    -----
        `datetime.timedelta`: The duration of the video.
    """
    frame_count = positive_int(frame_count)
    fps = positive_float(fps)
    return timedelta(seconds=frame_count / fps)


def convert_bytes(n: int) -> str:
    """
    Convert n bytes (int) to a human readable string.

    Usage:
    -----
    ```python
    >>> from videoxt.utils import convert_bytes
    >>> convert_bytes(1)
    '1.00 bytes'
    >>> convert_bytes(1024)
    '1.00 KB'
    >>> convert_bytes(1024**2)
    '1.00 MB'
    >>> convert_bytes(1024**3)
    '1.00 GB'
    >>> convert_bytes(1024**4)
    '1.00 TB'
    >>> convert_bytes(1024**5)
    '1.00 PB'
    ```

    Args:
    -----
        `n` (int): The number of bytes to convert.

    Returns:
    -----
        `str`: A human readable string representing the number of bytes.
    """
    n = positive_int(n)
    for size in ["bytes", "KB", "MB", "GB", "TB"]:
        if n < 1024.0:
            return f"{n:.2f} {size}"
        n /= 1024.0

    return f"{n:.2f} PB"


class CustomJSONEncoder(json.JSONEncoder):
    """A custom JSON encoder for types that are not JSON serializable."""

    def default(self, obj: Any) -> Any:
        """Return a JSON serializable representation of the object."""
        if isinstance(obj, Path):
            return obj.resolve().as_posix()
        if isinstance(obj, timedelta):
            return str(obj)
        if isinstance(obj, ExtractionMethod):
            return obj.value
        return super().default(obj)


@dataclass
class ToJsonMixin:
    """A mixin for dataclasses that can be represented as JSON."""

    def json(self, skip_private_keys: bool = False) -> str:
        """
        Return a JSON string representation of the dataclass.

        Args:
        -----
            `skip_private_keys` (bool):
                If True, private keys (keys starting with '_') are not included in the
                JSON string.

        Returns:
        -----
            `str`: JSON string representation of the dataclass.
        """
        d = remove_private_keys(asdict(self)) if skip_private_keys else asdict(self)
        return json.dumps(d, indent=2, cls=CustomJSONEncoder)

    def verbose_print(self, title: str) -> None:
        """Print the public keys of the JSON to console with a title."""
        color_map = {
            "PreparedRequest": "bright_magenta",
            "Result": "yellow",
        }
        color = color_map.get(title, "white")
        print(f"<[{color}]{title}[/{color}]>\n{self.json(skip_private_keys=True)}")


class DataclassType(Protocol):
    """Protocol representing dataclass attributes for type-hinting purposes."""

    __dataclass_fields__: ClassVar[dict[str, Any]]


def remove_private_keys(d: dict[str, Any]) -> dict[str, Any]:
    """
    Return a copy of the dictionary without private keys (keys starting with '_').

    Args:
    -----
        `d` (dict): The dictionary you want to remove private keys from.

    Returns:
    -----
        `dict[str, Any]`: A new dictionary containing public keys only.
    """
    copied_dict: defaultdict[str, Any] = defaultdict(dict)
    for k, v in d.items():
        if not k.startswith("_"):
            copied_dict[k] = remove_private_keys(v) if isinstance(v, dict) else v
    return dict(copied_dict)


def parse_kwargs(kwargs: dict[str, Any], obj: DataclassType) -> dict[str, Any]:
    """
    Return the keys and values in `kwargs` present in the `obj` dataclass attributes.

    Usage:
    -----
    ```python
    >>> from videoxt.utils import parse_kwargs
    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Test:
    ...     a: int
    ...     b: int
    >>> parse_kwargs({"a": 1, "b": 2, "c": 3}, Test)
    {'a': 1, 'b': 2}
    ```

    Args:
    -----
        `kwargs` (dict[str, Any]):
            A dictionary to filter down to keys present in the `obj` attributes.
        `obj` (dataclasses.dataclass):
            A dataclass to filter the `kwargs` dictionary with.

    Returns:
    -----
        `dict`: A dictionary of keyword arguments present in the `obj` attributes.
    """
    return {k: v for k, v in kwargs.items() if k in obj.__dataclass_fields__}
