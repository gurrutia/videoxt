"""Functions that prepare requests for extraction."""
import math
import typing as t
from dataclasses import dataclass
from pathlib import Path

import videoxt.utils as U


@dataclass
class TimeRange:
    """A dataclass to hold the time range for extraction."""

    start_timestamp: str
    start_second: float
    start_frame: int
    stop_timestamp: str
    stop_second: float
    stop_frame: int


def prepare_time_range(
    start_time_request: t.Union[float, str],
    stop_time_request: t.Optional[t.Union[float, str]],
    duration_timestamp: str,
    duration_seconds: float,
    video_frame_count: int,
    fps: float,
) -> TimeRange:
    """Prepare a TimeRange object to use for extraction.

    If a float is requested, the requested second is rounded to two decimal places,
    then used to calculate the timestamp and frame number.

    If a string representing a timestamp is requested, the timestamp is read as is,
    then converted to seconds which is used to calculate the frame number.

    If no stop time is requested, the video's length is used.
    """
    if isinstance(start_time_request, float):
        start_time = prepare_time_request_float(start_time_request, fps)
    else:
        start_time = prepare_time_request_str(start_time_request, fps)

    if stop_time_request is None:
        stop_time = duration_timestamp, duration_seconds, video_frame_count
    elif isinstance(stop_time_request, float):
        stop_time = prepare_time_request_float(stop_time_request, fps)
    else:
        stop_time = prepare_time_request_str(stop_time_request, fps)

    return TimeRange(
        start_timestamp=start_time[0],
        start_second=start_time[1],
        start_frame=start_time[2],
        stop_timestamp=stop_time[0],
        stop_second=stop_time[1],
        stop_frame=stop_time[2],
    )


def prepare_time_request_float(
    time_request: float, fps: float
) -> t.Tuple[str, float, int]:
    """Prepare the requested second by rounding it to two decimal places, then use it to
    calculate the timestamp and frame number.
    """
    second = round(time_request, 2)
    timestamp = U.seconds_to_timestamp(second)
    frame_num = prepare_frame_number(second, fps)

    return timestamp, second, frame_num


def prepare_time_request_str(time_request: str, fps: float) -> t.Tuple[str, float, int]:
    """Prepare the requested timestamp by reading it as is, then use it to calculate the
    second and frame number.
    """
    timestamp = time_request
    second = U.timestamp_to_seconds(timestamp)
    frame_num = prepare_frame_number(second, fps)

    return timestamp, second, frame_num


def prepare_frame_number(second: float, fps: float) -> int:
    """Prepare the start and stop frame numbers to use for extraction."""
    return math.floor(second * fps)


def prepare_fps(video_fps: float, request_fps: t.Optional[float]) -> float:
    """Prepare the fps to use for extraction. If no fps is requested, the video's fps is used."""
    return video_fps if request_fps is None else round(request_fps, 2)


def prepare_destdir(video_dir: Path, reqeust_dir: t.Optional[Path]) -> Path:
    """Prepare the directory to use for extraction. If no directory is requested,
    the video's directory is used.
    """
    return reqeust_dir or video_dir


def prepare_destdir_frames(
    video_dir: Path, video_filename: str, request_dir: t.Optional[Path]
) -> Path:
    """Prepare the directory to use for the 'frames' extraction request. If no directory
    is requested, a directory will be made within the video's directory.
    """
    if request_dir is None:
        return U.enumerate_dir(video_dir / f"{video_filename}_frames")

    return request_dir


def prepare_filename_frames(
    video_filename: str, request_filename: t.Optional[str]
) -> str:
    """Prepare the filename to use for the 'frames' extraction request. If no filename
    is requested, the video's filename is used.
    """
    return request_filename or video_filename


def prepare_filepath(
    video_filename: str, request_filename: t.Optional[str], dir: Path, suffix: str
) -> Path:
    """Prepare the filepath to use for extraction requests 'audio', 'clip', and 'gif'.
    If no filename was requested, the video's filename is used to create a new filepath.
    """
    if request_filename is None:
        return U.enumerate_filepath(dir / f"{video_filename}.{suffix}")

    return dir / f"{request_filename}.{suffix}"


def prepare_dimensions(
    video_dimensions: t.Tuple[int, int],
    request_dimensions: t.Optional[t.Tuple[int, int]],
    resize: float = 1.0,
) -> t.Tuple[int, int]:
    """Prepare the dimensions to use for extraction. If no dimensions are requested,
    the video's dimensions are used. If a resize value other than 1 was requested,
    the dimensions are multiplied by the resize factor.
    """
    dims = request_dimensions or video_dimensions

    if resize != 1:
        dims = tuple(int(dim * resize) for dim in dims)

    return dims


def prepare_images_expected(
    start_frame: int, stop_frame: int, capture_rate: int
) -> int:
    """Calculate the number of images expected to be extracted. Used to create a progress bar and
    to determine if the extraction was successful.
    """
    return math.ceil((stop_frame - start_frame) / capture_rate)


def prepare_filepath_image(
    dir: Path, filename: str, frame_num: int, image_format: str
) -> str:
    """Prepare the filepath to use for the 'frames' extraction request. The filepath is created
    by combining the directory, filename, frame number, and image format. The frame number is
    incremented by the capture rate during extraction.
    """
    image_filename = f"{filename}_{frame_num + 1}.{image_format}"
    return str(dir / image_filename)
