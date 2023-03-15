import datetime
from typing import Union


def timestamp_to_seconds(timestamp: str) -> int:
    """Converts a timestamp string to seconds. Milliseconds are truncated."""
    if "." in timestamp:
        timestamp = timestamp.split(".")[0]

    if ":" in timestamp:
        seconds = 0
        for value in timestamp.split(":"):
            seconds = seconds * 60 + int(value)
    else:
        seconds = int(timestamp)

    return seconds


def seconds_to_timestamp(seconds: Union[float, int]) -> str:
    """Converts seconds to a timestamp string. Milliseconds are truncated."""
    if seconds < 0:
        seconds = 0

    return str(datetime.timedelta(seconds=int(seconds)))
