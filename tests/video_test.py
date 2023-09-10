import typing as t
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


def test_video_capture_is_open_when_video_file_exists(tmp_video_filepath: Path):
    """Test that the `cv2.VideoCapture` object is opened when opening a video file.

    Args:
        tmp_video_filepath (Path): Filepath of the temporary video file.
    """
    with open_video_capture(tmp_video_filepath) as opencap:
        assert opencap.isOpened()


def test_video_properties_dataclass(video_properties: t.Dict[str, t.Any]):
    """Test that the `VideoProperties` dataclass is initialized as expected.

    `tmp_video_properties_cls` is created by the fixture of the same name in `conftest.py`.
    """
    video_properties_cls = VideoProperties(
        video_properties["dimensions"],
        video_properties["fps"],
        video_properties["frame_count"],
        video_properties["duration_seconds"],
        video_properties["duration_timestamp"],
        video_properties["suffix"],
    )
    assert isinstance(video_properties_cls, VideoProperties)
    assert video_properties_cls.dimensions == video_properties["dimensions"]
    assert video_properties_cls.fps == video_properties["fps"]
    assert video_properties_cls.frame_count == video_properties["frame_count"]
    assert video_properties_cls.duration_seconds == video_properties["duration_seconds"]
    assert (
        video_properties_cls.duration_timestamp
        == video_properties["duration_timestamp"]
    )
    assert video_properties_cls.suffix == video_properties["suffix"]


def test_get_video_properties(
    tmp_video_filepath: Path, video_properties: t.Dict[str, t.Any]
):
    """Test that the video properties are returned as expected.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    video_properties_cls = get_video_properties(tmp_video_filepath)
    assert isinstance(video_properties_cls, VideoProperties)
    assert video_properties_cls.dimensions == video_properties["dimensions"]
    assert video_properties_cls.fps == video_properties["fps"]
    assert video_properties_cls.frame_count == video_properties["frame_count"]
    assert video_properties_cls.duration_seconds == video_properties["duration_seconds"]
    assert (
        video_properties_cls.duration_timestamp
        == video_properties["duration_timestamp"]
    )
    assert video_properties_cls.suffix == video_properties["suffix"]


def test_video_dataclass(tmp_video_filepath: Path):
    """Test that the `Video` dataclass is initialized as expected with the
    correct properties.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.

    `tmp_video_properties_cls` is created by the fixture of the same name in `conftest.py`.
    """
    video = Video(tmp_video_filepath)
    assert isinstance(video, Video)
    assert isinstance(video.properties, VideoProperties)
