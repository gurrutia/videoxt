"""Pytest configuration file that contains fixtures and other configuration."""
import os
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
import pytest

from videoxt.video import open_video_capture
from videoxt.video import VideoProperties


@dataclass
class VideoSettings:
    """A dataclass to hold the settings of a temporary video file."""

    width: float
    height: float
    fps: float
    frame_count: int
    length_seconds: float
    length_timestamp: str
    suffix: str
    codec: str


@pytest.fixture
def tmp_video_settings() -> VideoSettings:
    """Create a temporary VideoSettings class and yield it.

    Yields:
        VideoSettings: A temporary VideoSettings class.
    """
    return VideoSettings(
        width=640,
        height=480,
        fps=30.0,
        frame_count=60,
        length_seconds=2.0,
        length_timestamp="0:00:02",
        suffix="mp4",
        codec="mp4v",
    )


@pytest.fixture
def tmp_video_filepath(tmp_path: Path, tmp_video_settings: VideoSettings) -> Path:
    """Create a temporary video file in the temporary directory and yield its path.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.

    Yields:
        Path: Filepath of the temporary video file.
    """
    tmp_filepath = tmp_path / "tmp.video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*tmp_video_settings.codec)
    video_writer = cv2.VideoWriter(
        str(tmp_filepath),
        fourcc,
        tmp_video_settings.fps,
        (tmp_video_settings.width, tmp_video_settings.height),
    )

    # Write frames to a video file to simulate a real video file.
    # The frames are just black images with the frame number written
    # on them.
    for i in range(
        int(tmp_video_settings.length_seconds) * int(tmp_video_settings.fps)
    ):
        frame = cv2.putText(
            np.zeros(
                (tmp_video_settings.height, tmp_video_settings.width, 3), dtype=np.uint8
            ),
            f"Frame {i + 1}",
            (240, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )
        video_writer.write(frame)
    video_writer.release()

    yield tmp_filepath

    if tmp_filepath.exists():
        os.remove(tmp_filepath)


@pytest.fixture
def tmp_video_capture(tmp_video_filepath: Path) -> cv2.VideoCapture:
    """Create a temporary `cv2.VideoCapture` object and yield it.

    Yields:
        cv2.VideoCapture: A temporary `cv2.VideoCapture` object.
    """
    with open_video_capture(tmp_video_filepath) as opencap:
        yield opencap


@pytest.fixture
def tmp_video_properties_cls(tmp_video_settings: VideoSettings) -> VideoProperties:
    """Create a temporary `VideoProperties` dataclass and yield it.

    Yields:
        VideoProperties: A temporary `VideoProperties` dataclass.
    """
    dimensions = (tmp_video_settings.width, tmp_video_settings.height)
    return VideoProperties(
        dimensions=dimensions,
        fps=tmp_video_settings.fps,
        frame_count=tmp_video_settings.frame_count,
        length_seconds=tmp_video_settings.length_seconds,
        length_timestamp=tmp_video_settings.length_timestamp,
        suffix=tmp_video_settings.suffix,
    )


@pytest.fixture
def tmp_text_filepath(tmp_path: Path) -> Path:
    """Create a temporary text file in the temporary directory and yield its path.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.

    Yields:
        Path: Filepath of the temporary text file.
    """
    tmp_filepath = tmp_path / "tmp_text.txt"
    content = "This is a temporary text file."
    with open(tmp_filepath, "w") as f:
        f.write(content)

    yield tmp_filepath

    if tmp_filepath.exists():
        os.remove(tmp_filepath)
