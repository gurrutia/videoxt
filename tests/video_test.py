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
def tmp_video_filepath() -> Path:
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

    # Write frames to a video file to simulate a real video file.
    # The frames are just black images with the frame number written
    # on them.
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
def tmp_video_capture(tmp_video_filepath: Path) -> cv2.VideoCapture:
    """Create a temporary `cv2.VideoCapture` object.

    Yields:
        cv2.VideoCapture: A temporary `cv2.VideoCapture` object.
    """
    with open_video_capture(tmp_video_filepath) as opencap:
        yield opencap


@pytest.fixture
def tmp_video_properties_cls() -> VideoProperties:
    return VideoProperties(
        dimensions=(640, 480),
        fps=30.0,
        frame_count=60,
        length_seconds=2.0,
        length_timestamp="0:00:02",
        suffix="mp4",
    )


@pytest.fixture
def tmp_text_filepath() -> Path:
    """Create a temporary text file for testing purposes.

    Yields:
        Path: Filepath of the temporary text file.
    """
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "tmp_text.txt")
    with open(temp_file, "w") as f:
        f.write("This is a temporary text file.")
    yield Path(temp_file)

    if os.path.exists(temp_file):
        os.remove(temp_file)
        os.rmdir(temp_dir)


def test_open_video_capture_when_file_exists(tmp_video_filepath: Path):
    """Test that the `cv2.VideoCapture` object is returned when opening a video file."""
    with open_video_capture(tmp_video_filepath) as opencap:
        assert isinstance(opencap, cv2.VideoCapture)


def test_open_video_capture_if_file_not_found(tmp_video_filepath: Path):
    """Test that FileNotFoundError is raised if the video file does not exist."""
    non_existing_file = tmp_video_filepath / "non_existing.mp4"
    with pytest.raises(FileNotFoundError):
        with open_video_capture(non_existing_file) as opencap:
            assert not opencap.isOpened()


def test_open_video_capture_if_file_exists_but_is_not_a_video_file(
    tmp_text_filepath: Path,
):
    """Test that TypeError is raised if an existing file is not a video file."""
    with pytest.raises(TypeError):
        with open_video_capture(tmp_text_filepath) as opencap:
            assert not opencap.isOpened()


def test_video_capture_is_open_when_video_file_exists(
    tmp_video_capture: cv2.VideoCapture,
):
    """Test that an open `cv2.VideoCapture` is detected as open."""
    assert tmp_video_capture.isOpened()


def test_video_properties_dataclass(tmp_video_properties_cls: VideoProperties):
    """Test that the `VideoProperties` dataclass is initialized as expected."""
    assert isinstance(tmp_video_properties_cls, VideoProperties)
    assert tmp_video_properties_cls.dimensions == (640, 480)
    assert tmp_video_properties_cls.fps == 30.0
    assert tmp_video_properties_cls.frame_count == 60
    assert tmp_video_properties_cls.length_seconds == 2.0
    assert tmp_video_properties_cls.length_timestamp == "0:00:02"
    assert tmp_video_properties_cls.suffix == "mp4"


def test_get_video_properties(tmp_video_filepath: Path):
    """Test that the video properties are returned as expected."""
    video_properties = get_video_properties(tmp_video_filepath)
    assert isinstance(video_properties, VideoProperties)
    assert video_properties.dimensions == (640, 480)
    assert video_properties.fps == 30.0
    assert video_properties.frame_count == 60
    assert video_properties.length_seconds == 2.0
    assert video_properties.length_timestamp == "0:00:02"
    assert video_properties.suffix == "mp4"


def test_video_dataclass(
    tmp_video_filepath: Path, tmp_video_properties_cls: VideoProperties
):
    """Test that the `Video` dataclass is initialized as expected with the correct properties."""
    video = Video(tmp_video_filepath)
    assert isinstance(video, Video)
    assert video.filepath == tmp_video_filepath
    assert video.properties == tmp_video_properties_cls
