import datetime
import typing as t
from pathlib import Path


def timestamp_to_seconds(timestamp: str) -> float:
    """Converts a timestamp string to seconds. Microseconds are truncated."""
    timestamp = timestamp.split(".")[0]
    parts = timestamp.split(":")
    seconds = sum(float(part) * 60**exp for exp, part in enumerate(reversed(parts)))

    return seconds


def seconds_to_timestamp(seconds: float) -> str:
    """Converts seconds to a timestamp string."""
    if seconds < 0:
        return "0:00:00"

    return str(datetime.timedelta(seconds=int(seconds)))


def enumerate_dir(dir_path: Path) -> Path:
    if not dir_path.exists():
        return dir_path

    index = 2
    while True:
        new_dir_path = dir_path.with_name(f"{dir_path.name} ({index})")
        if not new_dir_path.exists():
            return new_dir_path
        index += 1


def enumerate_filepath(filepath: Path) -> Path:
    """Enumerates a Path object filepath if it already exists."""
    if not filepath.exists():
        return filepath

    index = 2
    while True:
        new_filepath = filepath.with_name(f"{filepath.stem} ({index}){filepath.suffix}")
        if not new_filepath.exists():
            return new_filepath
        index += 1


def parse_kwargs(kwargs: t.Dict[str, t.Any], cls: t.Type[t.Any]) -> t.Dict[str, t.Any]:
    """Parse kwargs and return only the keywords that match a given class."""
    return {k: v for k, v in kwargs.items() if k in cls.__dataclass_fields__}
