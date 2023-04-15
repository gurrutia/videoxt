import os
import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest

from videoxt.video import get_video_properties
from videoxt.video import open_video_capture
from videoxt.video import Video
from videoxt.video import VideoProperties


@pytest.fixture(scope="function")
def tmp_video_file() -> Path:
    """Create a temporary video file for testing purposes.

    Yields:
        Path: Filepath of the temporary video file.
    """
    width = 640
    height = 480
    fps = 30.0
    duration_seconds = 2
    codec = "mp4v"

    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "tmp_video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(temp_file, fourcc, fps, (width, height))

    for i in range(duration_seconds * int(fps)):
        frame = cv2.putText(
            np.zeros((480, 640, 3), dtype=np.uint8),
            f"Frame {i + 1}",
            (240, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )
        out.write(frame)
    out.release()

    yield Path(temp_file)

    if os.path.exists(temp_file):
        os.remove(temp_file)
        os.rmdir(temp_dir)


@pytest.fixture
def tmp_video_capture(tmp_video_file):
    """Create a temporary `cv2.VideoCapture` object."""
    with open_video_capture(tmp_video_file) as opencap:
        yield opencap


def test_open_video_capture(tmp_video_file):
    """Test that a video capture object is returned"""
    with open_video_capture(tmp_video_file) as opencap:
        assert isinstance(opencap, cv2.VideoCapture)


def test_open_video_capture_context(tmp_video_capture):
    """Test that the video capture object is released after exiting the context"""
    assert tmp_video_capture.isOpened()


def test_open_video_capture_exception(tmp_video_file):
    """Test that an exception is raised when the video file does not exist"""
    non_existing_file = tmp_video_file / "non_existing.mp4"
    with pytest.raises(FileNotFoundError):
        with open_video_capture(non_existing_file) as opencap:
            assert not opencap.isOpened()


def test_video_properties_dataclass():
    """Test that the `VideoProperties` dataclass is initialized as expected."""
    video_properties = VideoProperties(
        dimensions=(640, 480),
        fps=30.0,
        frame_count=60,
        length_seconds=2.0,
        length_timestamp="0:00:02",
        suffix="mp4",
    )
    assert isinstance(video_properties, VideoProperties)
    assert video_properties.dimensions == (640, 480)
    assert video_properties.fps == 30.0
    assert video_properties.frame_count == 60
    assert video_properties.length_seconds == 2.0
    assert video_properties.length_timestamp == "0:00:02"
    assert video_properties.suffix == "mp4"


def test_get_video_properties(tmp_video_file):
    """Test that the video properties are returned as expected"""
    video_properties = get_video_properties(tmp_video_file)
    assert isinstance(video_properties, VideoProperties)
    assert video_properties.dimensions == (640, 480)
    assert video_properties.fps == 30.0
    assert video_properties.frame_count == 60
    assert video_properties.length_seconds == 2.0
    assert video_properties.length_timestamp == "0:00:02"
    assert video_properties.suffix == "mp4"


def test_video_dataclass(tmp_video_file):
    """Test that the `Video` dataclass is initialized as expected."""
    video_properties = VideoProperties(
        dimensions=(640, 480),
        fps=30.0,
        frame_count=60,
        length_seconds=2.0,
        length_timestamp="0:00:02",
        suffix="mp4",
    )
    video = Video(
        filepath=tmp_video_file,
    )
    assert isinstance(video, Video)
    assert video.filepath == tmp_video_file
    assert video.properties == video_properties
