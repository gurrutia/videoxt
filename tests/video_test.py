from pathlib import Path

import cv2
import pytest

from videoxt.exceptions import ValidationException
from videoxt.video import get_video_properties
from videoxt.video import open_video_capture
from videoxt.video import Video
from videoxt.video import VideoProperties


def test_open_video_capture_when_file_exists(tmp_video_filepath: Path):
    """Test that the `cv2.VideoCapture` object is returned when opening a video file.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    with open_video_capture(tmp_video_filepath) as opencap:
        assert isinstance(opencap, cv2.VideoCapture)


def test_open_video_capture_if_file_not_found(tmp_video_filepath: Path):
    """Test that FileNotFoundError is raised if the video file does not exist.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    non_existing_file = tmp_video_filepath / "non_existing.mp4"
    with pytest.raises(FileNotFoundError):
        with open_video_capture(non_existing_file) as opencap:
            assert not opencap.isOpened()


def test_open_video_capture_if_file_exists_but_is_not_a_video_file(
    tmp_text_filepath: Path,
):
    """Test that a TypeError is raised if an existing file is not a video file.

    `tmp_text_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    with pytest.raises(ValidationException):
        with open_video_capture(tmp_text_filepath) as opencap:
            assert not opencap.isOpened()


def test_video_capture_is_open_when_video_file_exists(
    tmp_video_capture: cv2.VideoCapture,
):
    """Test that an open `cv2.VideoCapture` is detected as open.

    `tmp_text_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    assert tmp_video_capture.isOpened()


def test_video_properties_dataclass(tmp_video_properties_cls: VideoProperties):
    """Test that the `VideoProperties` dataclass is initialized as expected.

    `tmp_video_properties_cls` is created by the fixture of the same name in `conftest.py`.
    """
    assert isinstance(tmp_video_properties_cls, VideoProperties)
    assert tmp_video_properties_cls.dimensions == (640, 480)
    assert tmp_video_properties_cls.fps == 30.0
    assert tmp_video_properties_cls.frame_count == 60
    assert tmp_video_properties_cls.length_seconds == 2.0
    assert tmp_video_properties_cls.length_timestamp == "0:00:02"
    assert tmp_video_properties_cls.suffix == "mp4"


def test_get_video_properties(tmp_video_filepath: Path):
    """Test that the video properties are returned as expected.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
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
    """Test that the `Video` dataclass is initialized as expected with the
    correct properties.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.

    `tmp_video_properties_cls` is created by the fixture of the same name in `conftest.py`.
    """
    video = Video(tmp_video_filepath)
    assert isinstance(video, Video)
    assert video.filepath == tmp_video_filepath
    assert video.properties == tmp_video_properties_cls
