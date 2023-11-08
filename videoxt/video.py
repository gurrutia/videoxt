"""Contains Video class and functions for validating and retrieving video properties."""
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path
from typing import Any

import cv2  # type: ignore
from moviepy.editor import VideoFileClip  # type: ignore

import videoxt.utils as U
import videoxt.validators as V
from videoxt.exceptions import (
    ClosedVideoCaptureError,
    ValidationError,
    VideoValidationError,
)


@dataclass
class Video:
    """
    Validate, set and store video properties such as the file path, dimensions, fps,
    frame count, duration, filesize, and whether the video has audio. A validated
    `Video` object is required to validate and calculate attributes in primary objects
    and functions throughout.

    Fields:
    -----
        `filepath` (Path): Path to the video file.

    Attributes:
    -----
        `dimensions` (tuple[int, int]):
            Dimensions of the video as (width, height).
        `fps` (float):
            Frame rate of the video.
        `frame_count` (int):
            Number of frames in the video.
        `duration` (datetime.timedelta):
            Duration of the video as a timedelta object.
        `duration_seconds` (float):
            Duration of the video in seconds.
        `duration_timestamp` (str):
            Duration of the video in `HH:MM:SS` format.
        `has_audio` (bool):
            True if the video has audio, False otherwise.
        `filesize_bytes` (int):
            Size of the video file in bytes.
        `filesize` (str):
            Size of the video file in a human-readable format.
    """

    filepath: Path
    dimensions: tuple[int, int] = field(init=False)
    fps: float = field(init=False)
    frame_count: int = field(init=False)
    duration: timedelta = field(init=False)
    duration_seconds: float = field(init=False)
    duration_timestamp: str = field(init=False)
    has_audio: bool = field(init=False)
    filesize_bytes: int = field(init=False)
    filesize: str = field(init=False)

    def __post_init__(self) -> None:
        """Run video file validations and set attributes read from a validated video."""
        self.validate_filepath()
        self.validate_filesize_bytes()
        self.setattrs_from_opencap()
        self.validate_dimensions()
        self.validate_fps()
        self.validate_frame_count()
        self.setattrs_duration()
        self.setattr_filesize()
        self.setattr_has_audio()

    def validate_filepath(self) -> Path:
        """Validate the file is a video file and exists."""
        self.filepath = V.valid_filepath(self.filepath, is_video=True)
        return self.filepath

    def validate_filesize_bytes(self) -> int:
        """Validate the video file size in bytes is a positive integer."""
        self.filesize_bytes = V.positive_int(self.filepath.stat().st_size)
        return self.filesize_bytes

    def setattrs_from_opencap(self) -> tuple[tuple[int, int], float, int]:
        """Set the dimensions, fps and frame count read from an opened video capture."""
        properties = fetch_video_properties(self.filepath)
        self.dimensions = properties.get("dimensions", None)
        self.fps = properties.get("fps", None)
        self.frame_count = properties.get("frame_count", None)

        return self.dimensions, self.fps, self.frame_count

    def validate_dimensions(self) -> tuple[int, int]:
        """Validate the video frame width and height are positive integers."""
        if self.dimensions is None:
            raise VideoValidationError(
                "The video dimensions could not be read from the video file. Please "
                "check the file."
            )

        try:
            self.dimensions = V.valid_dimensions(self.dimensions)
        except ValidationError as err:
            raise VideoValidationError(
                "The video dimensions are invalid. Please check the file."
            ) from err

        return self.dimensions

    def validate_fps(self) -> float:
        """Validate the video fps is a positive float."""
        if self.fps is None:
            raise VideoValidationError(
                "The video fps was read as None from the video file. Please check the "
                "file."
            )

        try:
            self.fps = V.positive_float(self.fps)
        except ValidationError as err:
            raise VideoValidationError(
                "The video fps was read as a non-positive float from the video file. "
                "Please check the file."
            ) from err

        return self.fps

    def validate_frame_count(self) -> int:
        """Validate the video frame count is a positive integer."""
        if self.frame_count is None:
            raise VideoValidationError(
                "The video frame count could not be read from the video file. Please "
                "check the file."
            )

        try:
            self.frame_count = V.positive_int(self.frame_count)
        except ValidationError as err:
            raise VideoValidationError(
                "The video frame count was read as a non-positive integer from the "
                "video file. Please check the file."
            ) from err

        return self.frame_count

    def setattrs_duration(self) -> tuple[timedelta, float, str]:
        """Set the duration attributes."""
        self.duration = U.calculate_duration(self.frame_count, self.fps)
        self.duration_seconds = self.duration.total_seconds()
        self.duration_timestamp = U.seconds_to_timestamp(self.duration_seconds)
        return self.duration, self.duration_seconds, self.duration_timestamp

    def setattr_filesize(self) -> str:
        """Set the filesize attribute to a human-readable format."""
        self.filesize = U.convert_bytes(self.filesize_bytes)
        return self.filesize

    def setattr_has_audio(self) -> bool:
        """Set the has_audio attribute with moviepy.editor import VideoFileClip.audio"""
        with VideoFileClip(str(self.filepath)) as clip:
            self.has_audio = bool(clip.audio)
        return self.has_audio


def fetch_video_properties(filepath: Path) -> dict[str, Any]:
    """
    Open the video file to retrieve and return the video's dimensions, fps, and frame
    count as a dictionary.

    Args:
    -----
        `filepath` (Path): Path to the video file.

    Returns:
    -----
        `dict[str, Any]`:
            Dictionary containing unvalidated video properties:

            - "dimensions" (tuple): Dimensions of the video as (width, height).
            - "fps" (float): Frame rate of the video.
            - "frame_count" (int): Number of frames in the video.
    """
    with open_video_capture(filepath) as opencap:
        frame_height: int = opencap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_width: int = opencap.get(cv2.CAP_PROP_FRAME_WIDTH)
        fps: float = opencap.get(cv2.CAP_PROP_FPS)
        frame_count: int = opencap.get(cv2.CAP_PROP_FRAME_COUNT)

    return {
        "dimensions": (frame_width, frame_height),
        "fps": fps,
        "frame_count": frame_count,
    }


@contextmanager
def open_video_capture(filepath: Path) -> Iterator[cv2.VideoCapture]:
    """
    Context manager for opening a video file with `cv2.VideoCapture`.

    Usage:
    -----
    ```python
    >>> from videoxt.video import open_video_capture
    >>> with open_video_capture('path/to/video.mp4') as opencap:
    ...     # do something with 'opencap'
    ...     type(opencap)
    <class 'cv2.VideoCapture'>
    ```

    Args:
    -----
        `filepath` (Path): Path to the video file.

    Yields:
    -----
        `cv2.VideoCapture`: An opened cv2 video capture.

    Raises:
    -----
        - `ClosedVideoCaptureError`:
            - If `cv2.VideoCapture().isOpened()` returns False.
            - If a `cv2.error` occurred while opening a `cv2.VideoCapture()`.
            - For more details see:
            https://docs.opencv.org/4.8.0/d8/dfe/classcv_1_1VideoCapture.html
    """
    try:
        video_capture = cv2.VideoCapture(str(filepath))
        if not video_capture.isOpened():
            raise ClosedVideoCaptureError(
                "Unable to open the video file or maintain it in an open state. Please "
                "check the file.\ncv2.VideoCapture().isOpened() returned False."
            )

    except cv2.error as err:
        raise ClosedVideoCaptureError(
            "A cv2.error occurred while opening a cv2.VideoCapture(). "
            f"Please check the file, got {filepath!r}"
        ) from err

    else:
        yield video_capture

    finally:
        try:
            video_capture.release()
        except UnboundLocalError:
            pass  # Ctrl+C keyboard interrupt
