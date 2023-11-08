import cv2  # type: ignore
import pytest

from videoxt.exceptions import ClosedVideoCaptureError, VideoValidationError
from videoxt.video import Video, fetch_video_properties, open_video_capture


def test_open_video_capture_if_filepath_as_path_and_is_valid_video_file(
    fixture_tmp_video_filepath,
):
    with open_video_capture(fixture_tmp_video_filepath) as opencap:
        assert opencap.isOpened()
        assert isinstance(opencap, cv2.VideoCapture)


def test_open_video_capture_if_filepath_as_str_and_is_valid_video_file(
    fixture_tmp_video_filepath,
):
    with open_video_capture(str(fixture_tmp_video_filepath)) as opencap:
        assert opencap.isOpened()
        assert isinstance(opencap, cv2.VideoCapture)


def test_open_video_capture_if_filepath_is_none():
    with pytest.raises(ClosedVideoCaptureError):
        with open_video_capture(None) as opencap:
            assert not opencap.isOpened()


def test_open_video_capture_if_filepath_is_int():
    with pytest.raises(ClosedVideoCaptureError):
        with open_video_capture(1) as opencap:
            assert not opencap.isOpened()


def test_open_video_capture_if_filepath_doesnt_exist(fixture_tmp_dir):
    non_existing_file = fixture_tmp_dir / "non_existing.mp4"
    with pytest.raises(ClosedVideoCaptureError):
        with open_video_capture(non_existing_file) as opencap:
            assert not opencap.isOpened()


def test_open_video_capture_if_filepath_is_a_directory(fixture_tmp_dir):
    with pytest.raises(ClosedVideoCaptureError):
        with open_video_capture(fixture_tmp_dir) as opencap:
            assert not opencap.isOpened()


def test_open_video_capture_if_filepath_is_an_existing_text_file(
    fixture_tmp_text_filepath,
):
    with pytest.raises(ClosedVideoCaptureError):
        with open_video_capture(fixture_tmp_text_filepath) as opencap:
            assert not opencap.isOpened()


def test_open_video_capture_if_filepath_is_a_video_file_with_zero_second_duration(
    fixture_tmp_video_filepath_zero_seconds,
):
    with pytest.raises(ClosedVideoCaptureError):
        with open_video_capture(fixture_tmp_video_filepath_zero_seconds) as opencap:
            assert not opencap.isOpened()


def test_fetch_video_properties_if_filepath_is_valid_video_file(
    fixture_tmp_video_filepath, fixture_tmp_video_properties
):
    fetched_properties = fetch_video_properties(fixture_tmp_video_filepath)
    assert isinstance(fetched_properties, dict)
    assert (
        fetched_properties["dimensions"] == fixture_tmp_video_properties["dimensions"]
    )
    assert fetched_properties["fps"] == fixture_tmp_video_properties["fps"]
    assert (
        fetched_properties["frame_count"] == fixture_tmp_video_properties["frame_count"]
    )


def test_video_object_is_instance_of_video_dataclass(fixture_tmp_video_filepath):
    video = Video(fixture_tmp_video_filepath)
    assert isinstance(video, Video)


def test_video_object_attributes_match_expected_values(
    fixture_tmp_video_filepath, fixture_tmp_video_properties
):
    video = Video(fixture_tmp_video_filepath)
    assert video.filepath == fixture_tmp_video_filepath
    assert video.dimensions == fixture_tmp_video_properties["dimensions"]
    assert video.fps == fixture_tmp_video_properties["fps"]
    assert video.frame_count == fixture_tmp_video_properties["frame_count"]
    assert video.duration == fixture_tmp_video_properties["duration"]
    assert video.duration_seconds == fixture_tmp_video_properties["duration_seconds"]
    assert (
        video.duration_timestamp == fixture_tmp_video_properties["duration_timestamp"]
    )
    assert video.has_audio == fixture_tmp_video_properties["has_audio"]
    assert (
        video.filesize_bytes
        == fixture_tmp_video_properties["video_file_path"].stat().st_size
    )


def test_video_object_with_invalid_filepath_raises_cv2_error(
    fixture_tmp_video_filepath_zero_seconds,
):
    with pytest.raises(ClosedVideoCaptureError):
        Video(fixture_tmp_video_filepath_zero_seconds)


def test_video_object_validate_dimensions_raises_video_validation_error_if_dimensions_are_none(
    fixture_tmp_video_filepath,
):
    video = Video(fixture_tmp_video_filepath)
    video.dimensions = None
    with pytest.raises(VideoValidationError):
        video.validate_dimensions()


def test_video_object_validate_dimensions_raises_video_validation_error_if_dimensions_are_zero(
    fixture_tmp_video_filepath,
):
    video = Video(fixture_tmp_video_filepath)
    video.dimensions = (0, 0)
    with pytest.raises(VideoValidationError):
        video.validate_dimensions()


def test_video_object_validate_fps_raises_video_validation_error_if_fps_is_none(
    fixture_tmp_video_filepath,
):
    video = Video(fixture_tmp_video_filepath)
    video.fps = None
    with pytest.raises(VideoValidationError):
        video.validate_fps()


def test_video_object_validate_fps_raises_video_validation_error_if_fps_is_zero(
    fixture_tmp_video_filepath,
):
    video = Video(fixture_tmp_video_filepath)
    video.fps = 0
    with pytest.raises(VideoValidationError):
        video.validate_fps()


def test_video_object_validate_frame_count_raises_video_validation_error_if_frame_count_is_none(
    fixture_tmp_video_filepath,
):
    video = Video(fixture_tmp_video_filepath)
    video.frame_count = None
    with pytest.raises(VideoValidationError):
        video.validate_frame_count()


def test_video_object_validate_frame_count_raises_video_validation_error_if_frame_count_is_zero(
    fixture_tmp_video_filepath,
):
    video = Video(fixture_tmp_video_filepath)
    video.frame_count = 0
    with pytest.raises(VideoValidationError):
        video.validate_frame_count()


def test_fetch_video_properties_with_invalid_filepath_raises_cv2_error(
    fixture_tmp_video_filepath_zero_seconds,
):
    with pytest.raises(ClosedVideoCaptureError):
        fetch_video_properties(fixture_tmp_video_filepath_zero_seconds)
