import cv2
import pytest

from videoxt.video import open_video_capture


@pytest.fixture
def tmp_video_file(tmp_path):
    """Create a temporary video file"""
    video_file = tmp_path / "test_video.mp4"
    video_file.touch()
    yield video_file
    video_file.unlink()


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
    assert not tmp_video_capture.isOpened()


def test_open_video_capture_exception(tmp_video_file):
    """Test that an exception is raised when the video file does not exist"""
    non_existing_file = tmp_video_file / "non_existing.mp4"
    with pytest.raises(FileNotFoundError):
        with open_video_capture(non_existing_file) as opencap:
            pass
