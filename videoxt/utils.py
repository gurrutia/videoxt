import datetime
import typing as t
from pathlib import Path


def timestamp_to_seconds(timestamp: str) -> float:
    """Converts a timestamp string to seconds. Microseconds are truncated.

    Examples:
        >>> timestamp_to_seconds("0:00")
        0.0
        >>> timestamp_to_seconds("0:59")
        59.0
        >>> timestamp_to_seconds("1:01")
        61.0
        >>> timestamp_to_seconds("1:01.123456")
        61.0

    Args:
        timestamp: A timestamp string in the format "HH:MM:SS" or "SS".

    Returns:
        float: The number of seconds represented by the timestamp.
    """
    timestamp = timestamp.split(".")[0]
    parts = timestamp.split(":")
    seconds = sum(float(part) * 60**exp for exp, part in enumerate(reversed(parts)))

    return seconds


def seconds_to_timestamp(seconds: float) -> str:
    """Converts seconds to a timestamp string. Microseconds are truncated.

    Examples:
        >>> seconds_to_timestamp(0)
        '0:00:00'
        >>> seconds_to_timestamp(59)
        '0:00:59'
        >>> seconds_to_timestamp(61)
        '0:01:01'
        >>> seconds_to_timestamp(61.123456)
        '0:01:01'

    Args:
        seconds: The number of seconds to convert represented by a float.

    Returns:
        str: A timestamp string in the format "HH:MM:SS".
    """
    if seconds <= 0:
        return "0:00:00"

    return str(datetime.timedelta(seconds=int(seconds)))


def enumerate_dir(dir_path: Path) -> Path:
    """Returns a Path object with an enumerated name if a directory with the same
    name already exists. If the directory does not exist, the original path is returned.

    Examples:
        >>> enumerate_dir(Path("test_dir"))
        Path('test_dir')
        >>> enumerate_dir(Path("test_dir"))
        Path('test_dir (2)')
        >>> enumerate_dir(Path("test_dir (2)"))
        Path('test_dir (3)')

    Args:
        dir_path: The path to the directory to enumerate.

    Returns:
        Path: A Path object with an enumerated name if a directory with the same
            name already exists. If the directory does not exist, the original path is
            returned.
    """
    if not dir_path.exists():
        return dir_path

    index = 2
    while True:
        new_dir_path = dir_path.with_name(f"{dir_path.name} ({index})")
        if not new_dir_path.exists():
            return new_dir_path
        index += 1


def enumerate_filepath(filepath: Path) -> Path:
    """Returns new Path object with an enumerated name if a file with the same name
    already exists. If the file does not exist, the original path is returned.

    Examples:
        >>> enumerate_filepath(Path("test.txt"))
        Path('test.txt')
        >>> enumerate_filepath(Path("test.txt"))
        Path('test (2).txt')
        >>> enumerate_filepath(Path("test (2).txt"))
        Path('test (3).txt')

    Args:
        filepath: The path to the file to enumerate.

    Returns:
        Path: A Path object with an enumerated name if a file with the same name
            already exists. If the file does not exist, the original path is returned.
    """
    if not filepath.exists():
        return filepath

    index = 2
    while True:
        new_filepath = filepath.with_name(f"{filepath.stem} ({index}){filepath.suffix}")
        if not new_filepath.exists():
            return new_filepath
        index += 1


def parse_kwargs(kwargs: t.Dict[str, t.Any], cls: t.Type[t.Any]) -> t.Dict[str, t.Any]:
    """Parses a dictionary of keyword arguments and returns only those that match a
    given dataclass.

    Example:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Test:
        ...     a: int
        ...     b: int
        >>> parse_kwargs({"a": 1, "b": 2, "c": 3}, Test)
        {'a': 1, 'b': 2}

    Args:
        kwargs: A dictionary of keyword arguments you want to parse.
        cls: The dataclass to match the keyword arguments against.

    Returns:
        dict: A dictionary of keyword arguments that match the given dataclass.
    """
    return {k: v for k, v in kwargs.items() if k in cls.__dataclass_fields__}
