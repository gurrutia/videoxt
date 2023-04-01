"""Functions that prepare requests for extraction."""
import math
import typing as t
from dataclasses import dataclass
from pathlib import Path

import videoxt.utils as U


@dataclass
class TimeRange:
    start_timestamp: str
    start_frame: int
    start_second: float
    stop_timestamp: str
    stop_frame: int
    stop_second: float


def prepare_time_range(
    start_time_request: t.Union[float, str],
    stop_time_request: t.Optional[t.Union[float, str]],
    video_length_timestamp: str,
    video_length_seconds: float,
    video_frame_count: int,
    fps: float,
) -> TimeRange:
    start_frame = prepare_time_range_frame(start_time_request, fps)
    start_second = prepare_seconds(start_frame, fps)
    start_timestamp = U.seconds_to_timestamp(start_second)

    if stop_time_request is None:
        stop_timestamp = video_length_timestamp
        stop_frame = video_frame_count
        stop_second = video_length_seconds
    else:
        stop_frame = prepare_time_range_frame(stop_time_request, fps)
        stop_second = prepare_seconds(stop_frame, fps)
        stop_timestamp = U.seconds_to_timestamp(stop_second)

    return TimeRange(
        start_timestamp=start_timestamp,
        start_frame=start_frame,
        start_second=start_second,
        stop_timestamp=stop_timestamp,
        stop_frame=stop_frame,
        stop_second=stop_second,
    )


def prepare_time_range_frame(time_request: t.Union[float, str], fps: float) -> int:
    seconds = (
        U.timestamp_to_seconds(time_request)
        if isinstance(time_request, str)
        else time_request
    )

    return math.floor(seconds * fps)


def prepare_seconds(frame: int, fps: float) -> float:
    return round(frame / fps, 2)


def prepare_fps(video_fps: float, request_fps: t.Optional[float]) -> float:
    return video_fps if request_fps is None else request_fps


def prepare_frame_number(fps: float, second: float) -> int:
    return int(second * fps)


def prepare_destdir(video_dir: Path, reqeust_dir: t.Optional[Path]) -> Path:
    """Prepare the directory to use for extraction. If no directory is requested,
    the video's directory is used.
    """
    return reqeust_dir or video_dir


def prepare_destdir_frames(
    video_dir: Path, video_filename: str, request_dir: t.Optional[Path]
) -> Path:
    if request_dir is None:
        return U.enumerate_dir(video_dir / f"{video_filename}_frames")

    return request_dir


def prepare_filename_frames(video_stem: str, request_filename: t.Optional[str]) -> str:
    return request_filename or video_stem


def prepare_filepath(
    video_filename: str, request_filename: t.Optional[str], dir: Path, suffix: str
) -> Path:
    if request_filename is None:
        return U.enumerate_filepath(dir / f"{video_filename}.{suffix}")

    return dir / f"{request_filename}.{suffix}"


def prepare_dimensions(
    video_dimensions: t.Tuple[int, int],
    request_dimensions: t.Optional[t.Tuple[int, int]],
    resize: float = 1.0,
) -> t.Tuple[int, int]:
    dims = request_dimensions or video_dimensions

    if resize != 1:
        dims = tuple(int(dim * resize) for dim in dims)

    return dims


def prepare_images_expected(
    start_frame: int, stop_frame: int, capture_rate: int
) -> int:
    return math.ceil((stop_frame - start_frame) / capture_rate)


def prepare_filepath_image(
    dir: Path, filename: str, frame: int, image_format: str
) -> str:
    image_filename = f"{filename}_{frame + 1}.{image_format}"
    return str(dir / image_filename)
