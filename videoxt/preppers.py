"""Contains functions, objects that prepare shared request values for extraction."""
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import videoxt.utils as U
import videoxt.validators as V


@dataclass
class ExtractionRange:
    """
    Container for variations of the user's requested extraction range.

    The range is represented in seconds, as timestamps, and frame numbers. Validations
    and preparations are run on init.

    Attributes:
    -----
        `start_request` (float | int | str):
            Start time of the extraction in seconds or as a timestamp (`HH:MM:SS`).
        `stop_request` (float | int | str):
            Stop time of the extraction in seconds or as a timestamp (`HH:MM:SS`).
        `duration_seconds` (float):
            Duration of the video in seconds.
        `frame_count` (int):
            Number of frames in the video.
        `fps` (float):
            Frames per second to use for extraction.

    Usage:
    -----
    >>> from videoxt.preppers import ExtractionRange
    >>> extraction_range = ExtractionRange(
    ...     start_request=0,
    ...     stop_request=10,
    ...     fps=30,
    ...     frame_count=600,
    ...     duration_seconds=20,
    ... )
    >>> extraction_range.start_second
    0
    >>> extraction_range.stop_second
    10
    >>> extraction_range.start_timestamp
    '0:00:00'
    >>> extraction_range.stop_timestamp
    '0:00:10'
    >>> extraction_range.start_frame
    0
    >>> extraction_range.stop_frame
    300
    """

    start_request: float | int | str
    stop_request: float | int | str
    duration_seconds: float = field(repr=False)
    frame_count: int = field(repr=False)
    fps: float = field(repr=False)
    start_second: float = field(init=False)
    stop_second: float = field(init=False)
    start_timestamp: str = field(init=False)
    stop_timestamp: str = field(init=False)
    start_frame: int = field(init=False)
    stop_frame: int = field(init=False)

    def __post_init__(self):
        """
        Start procedure that prepares and validates the extraction range.

        - Convert the requested start and stop times to seconds (float)
        - Validate the range against the video's duration
        - Convert each request second to timestamps (str) and frame numbers (int).
        """
        self._prepare_start_second()
        self._prepare_stop_second()
        self._validate_range()
        self._prepare_start_timestamp()
        self._prepare_stop_timestamp()
        self._prepare_start_frame()
        self._prepare_stop_frame()

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary of the validated extraction start and stop points."""
        return {
            "start_second": self.start_second,
            "stop_second": self.stop_second,
            "start_timestamp": self.start_timestamp,
            "stop_timestamp": self.stop_timestamp,
            "start_frame": self.start_frame,
            "stop_frame": self.stop_frame,
        }

    def _prepare_start_second(self) -> float:
        """Convert the start time requested to seconds (float)."""
        self.start_second = (
            float(self.start_request)
            if isinstance(self.start_request, (float, int))
            else U.timestamp_to_seconds(self.start_request)
        )
        return self.start_second

    def _prepare_stop_second(self) -> float:
        """Convert the stop time requested to seconds (float)."""
        self.stop_second = (
            float(self.stop_request)
            if isinstance(self.stop_request, (float, int))
            else U.timestamp_to_seconds(self.stop_request)
        )
        return self.stop_second

    def _validate_range(self) -> tuple[float, float, float]:
        """
        Validate start and stop seconds against the video's duration and each other.

        Returns:
        -----
            `tuple[float, float, float]`: Validated (start, stop, duration) in seconds.
        """
        start, stop, duration = V.valid_extraction_range(
            self.start_second, self.stop_second, self.duration_seconds
        )
        return start, stop, duration

    def _prepare_start_timestamp(self) -> str:
        """Convert the start time requested to a timestamp (str) `HH:MM:SS`."""
        self.start_timestamp = (
            self.start_request
            if isinstance(self.start_request, str)
            else U.seconds_to_timestamp(self.start_request)
        )
        return self.start_timestamp

    def _prepare_stop_timestamp(self) -> str:
        """Convert the stop time requested to a timestamp (str) `HH:MM:SS`."""
        self.stop_timestamp = (
            self.stop_request
            if isinstance(self.stop_request, str)
            else U.seconds_to_timestamp(self.stop_request)
        )
        return self.stop_timestamp

    def _prepare_start_frame(self) -> int:
        """Convert the start time requested to a frame number (int)."""
        self.start_frame = math.floor(self.start_second * self.fps)
        return self.start_frame

    def _prepare_stop_frame(self) -> int:
        """Convert the stop time requested to a frame number (int)."""
        self.stop_frame = (
            self.frame_count
            if self.stop_second is None
            else math.floor(self.stop_second * self.fps)
        )
        return self.stop_frame


def prepare_extraction_range(
    start_request: float | int | str,
    stop_request: float | int | str,
    duration_seconds: float,
    frame_count: int,
    fps: float,
) -> dict[str, Any]:
    """
    Return a dictionary representing a validated extraction start and stop points.

    The dictionary contains variations of the requested start and stop times as seconds
    (float), timestamps (str), and frame numbers (int); including the requested values.

    Args:
    -----
        `start_request` (float | int | str):
            Start time of the extraction in seconds or as a timestamp (`HH:MM:SS`).
        `stop_request` (float | int | str):
            Stop time of the extraction in seconds or as a timestamp (`HH:MM:SS`).
        `duration_seconds` (float):
            Duration of the video in seconds.
        `frame_count` (int):
            Number of frames in the video.
        `fps` (float):
            Frames per second to use for extraction.

    Returns:
    -----
        `dict[str, Any]`: Dictionary of validated extraction start and stop points.
    """
    extraction_range = ExtractionRange(
        start_request=start_request,
        stop_request=stop_request,
        duration_seconds=duration_seconds,
        frame_count=frame_count,
        fps=fps,
    )

    return extraction_range.to_dict()


def prepare_dimensions(
    video_dimensions: tuple[int, int],
    resize: float,
    request_dimensions: Optional[tuple[int, int]] = None,
) -> tuple[int, int]:
    """
    Prepare validated dimensions for extraction considering resize factor.

    Args:
    -----
        `video_dimensions` (tuple[int, int]):
            Dimensions of the video.
        `resize` (float):
            Resize factor to apply to the video.
        `request_dimensions` (Optional[tuple[int, int]]):
            Optional dimensions to use. Defaults to None.

    Returns:
    -----
        `tuple[int, int]`: Dimensions to use for extraction.
    """
    dims = request_dimensions or video_dimensions

    if resize != 1.0:
        dims = (int(dims[0] * resize), int(dims[1] * resize))

    return dims


def prepare_destpath(
    video_filepath: Path,
    suffix: str,
    request_filename: Optional[str] = None,
    request_dir: Optional[Path] = None,
    overwrite: bool = False,
) -> Path:
    """
    Construct and return the destination path for the extracted file.

    Args:
    -----
        `video_filepath` (pathlib.Path):
            Path to the video file.
        `request_suffix` (str):
            Required file suffix to use (with or without the leading '.').
        `request_filename` (Optional[str]):
            Optional filename to use. Defaults to None.
        `request_destdir` (Optional[pathlib.Path]):
            Optional directory to save the processed file. Defaults to None.
        `overwrite` (bool):
            If True, allows overwriting an existing file with the same name.
            Defaults to False.

    Returns:
    -----
        `pathlib.Path`: Path to the destination file.

    Notes:
    -----
        - Uses `request_filename` with the specified `suffix` if provided; otherwise,
            uses video file's name.
        - Saves the file in `request_dir` if provided; otherwise, saves in the video's
            directory.
        - Handles overwriting: if `overwrite` is True, may overwrite existing file with
            the same name; if False, ensures a unique filename before saving.
    """
    base_dir = request_dir or video_filepath.parent
    suffix = suffix if suffix.startswith(".") else f".{suffix}"

    if request_filename:
        filename = f"{request_filename}{suffix}"
    else:
        filename = f"{video_filepath.stem}{suffix}"

    dest_path = base_dir / filename

    if overwrite is True and dest_path != video_filepath:
        return dest_path
    else:
        return U.enumerate_filepath(dest_path, label="_vxt")


def prepare_start_time(
    request_start_time: Optional[float | int | str] = None,
) -> float | int | str:
    """
    Return the start time requested or 0 if not provided.

    Args:
    -----
        `request_start_time` (Optional[float | int | str]):
            Optional start time requested. Defaults to None.

    Returns:
    -----
        `float | int | str`: The start time requested or 0 if not provided.
    """
    return request_start_time if request_start_time is not None else 0
