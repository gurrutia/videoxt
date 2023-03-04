import datetime


def timestamp_to_seconds(timestamp: str) -> int:
    if ":" in timestamp:
        seconds = 0
        for value in timestamp.split(":"):
            seconds = seconds * 60 + int(value)
    else:
        seconds = int(timestamp)

    return seconds


def seconds_to_timestamp(seconds: int) -> str:
    return str(datetime.timedelta(seconds=seconds))
