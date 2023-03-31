import typing as t
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

import cv2  # type: ignore

import videoxt.preppers as P
import videoxt.utils as U
import videoxt.validators as V


@dataclass
class VideoProperties:
    dimensions: t.Tuple[int, int]
    fps: float
    frame_count: int
    length_seconds: float
    length_timestamp: str
    suffix: str


def get_video_properties(video_filepath: Path) -> VideoProperties:
    """Gets video properties from a video filepath.

    Properties include: dimensions, fps, frame count, length in seconds, and length as a timestamp.

    Returns: `VideoProperties` object.
    """
    suffix = video_filepath.suffix[1:]

    video_capture = cv2.VideoCapture(str(video_filepath))
    fps = round(video_capture.get(cv2.CAP_PROP_FPS), 2)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    dimensions = (
        int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )

    video_capture.release()

    length_seconds = P.prepare_seconds(frame_count, fps)
    length_timestamp = U.seconds_to_timestamp(length_seconds)

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
        self.filepath = V.valid_filepath(self.filepath)
        self.properties = get_video_properties(self.filepath)

    def __str__(self) -> str:
        import videoxt.displays

        return videoxt.displays.video_str(self)
