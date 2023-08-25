import typing as t
from contextlib import contextmanager
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

import cv2  # type: ignore

import videoxt.utils as U
import videoxt.validators as V


@contextmanager
def open_video_capture(video_filepath: Path) -> t.Iterator[cv2.VideoCapture]:
    """A context manager for `cv2.VideoCapture` objects.

    Yields:
    -------
    `cv2.VideoCapture`

    Example:
    --------
    >>> from videoxt import Video
    >>> with open_video_capture('path/to/video.mp4') as opencap:
    ...     # do something with opencap
    """
    if not video_filepath.exists():
        raise FileNotFoundError(f"Video file not found: {video_filepath}")

    if not V.is_video_file(video_filepath):
        raise TypeError(f"File is not a video file: {video_filepath}")

    cap = cv2.VideoCapture(str(video_filepath))

    if not cap.isOpened():
        raise TypeError(f"Could not open video file: {video_filepath}")

    try:
        yield cap
    finally:
        cap.release()


@dataclass
class VideoProperties:
    """A dataclass to hold the properties of a video."""

    dimensions: t.Tuple[int, int]
    fps: float
    frame_count: int
    length_seconds: float
    length_timestamp: str
    suffix: str


def get_video_properties(video_filepath: Path) -> VideoProperties:
    """Get video properties from a video filepath using `cv2.VideoCapture`.

    Parameters:
    -----------
    `video_filepath` : Path
        Path to the video file with the extension.

    Returns:
    --------
    `VideoProperties`
    """
    with open_video_capture(video_filepath) as opencap:
        fps = round(opencap.get(cv2.CAP_PROP_FPS), 2)
        frame_count = int(opencap.get(cv2.CAP_PROP_FRAME_COUNT))
        dimensions = (
            int(opencap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(opencap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )

    length_seconds = round(frame_count / fps, 2)
    length_timestamp = U.seconds_to_timestamp(length_seconds)
    suffix = video_filepath.suffix[1:]

    return VideoProperties(
        dimensions=dimensions,
        fps=fps,
        frame_count=frame_count,
        length_seconds=length_seconds,
        length_timestamp=length_timestamp,
        suffix=suffix,
    )


@dataclass
class Video:
    """Video object required for all extraction methods.

    Parameters
    ----------
    `filepath` (required) : Path
        Path to the video file with the extension.

    Attributes
    ----------
    `properties` : VideoProperties
        `dimensions` : Tuple[int, int]
            The dimensions of the video as a tuple (width, height).
        `length_timestamp` : str
            The length of the video in the format `H:MM:SS`.
        `length_seconds` : float
            The length of the video in seconds.
        `fps` : float
            The frame rate of the video.
        `frame_count` : int
            The number of frames in the video.
        `suffix` : str
            The file extension of the video without the period.
    """

    filepath: Path
    properties: VideoProperties = field(init=False)

    def __post_init__(self) -> None:
        """Validate the filepath and get the video properties."""
        self.filepath = V.valid_filepath(self.filepath)
        self.properties = get_video_properties(self.filepath)

    def open_capture(self) -> cv2.VideoCapture:
        """Open the video capture object for the video.

        Returns:
        --------
        `cv2.VideoCapture`
        """
        return open_video_capture(self.filepath)

    def __str__(self) -> str:
        import videoxt.displays

        return videoxt.displays.video_str(self)
