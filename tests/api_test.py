import typing as t

import pytest

from videoxt.utils import parse_kwargs
from videoxt.video import VideoProperties


@pytest.mark.usefixtures("extracted_frames", "video_properties")
class TestExtractFrames:
    """Tests for the extract_frames function. The `extracted_frames` fixture
    calls the extract_frames function with no arguments and yields the results.

    Args:
        extracted_frames (t.Dict[str, t.Any]):
            The results of the `extract_frames` function with no arguments.
        video_properties (t.Dict[str, t.Any]):
            The properties of the video used to validate the results.
    """

    def test_extract_frames_valid_default_request_success_is_true(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["success"] is True

    def test_extract_frames_valid_default_request_video_filepath(
        self, extracted_frames: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
    ):
        assert (
            extracted_frames["request"]["video"]["filepath"]
            == video_properties["video_file_path"]
        )

    def test_extract_frames_valid_default_request_video_properties(
        self, extracted_frames: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
    ):
        expected_properties = parse_kwargs(video_properties, VideoProperties)
        assert extracted_frames["request"]["video"]["properties"] == expected_properties

    def test_extract_frames_valid_default_request_start_time(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["start_time"] == "0:00:00"

    def test_extract_frames_valid_default_request_stop_time(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["stop_time"] is None

    def test_extract_frames_valid_default_request_fps(
        self, extracted_frames: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["fps"] == video_properties["fps"]

    def test_extract_frames_valid_default_request_destdir(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["destdir"].exists()

    def test_extract_frames_valid_default_request_filename(
        self, extracted_frames: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["filename"] == video_properties["filename"]

    def test_extract_frames_valid_default_request_verbose(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["verbose"] is False

    def test_extract_frames_valid_default_request_time_range_start_timestamp(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["time_range"]["start_timestamp"] == "0:00:00"

    def test_extract_frames_valid_default_request_time_range_start_frame(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["time_range"]["start_frame"] == 0

    def test_extract_frames_valid_default_request_time_range_start_second(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["time_range"]["start_second"] == 0.0

    def test_extract_frames_valid_default_request_time_range_stop_timestamp(
        self,
        extracted_frames: t.Dict[str, t.Any],
    ):
        assert extracted_frames["request"]["time_range"]["stop_timestamp"] == "0:00:02"

    def test_extract_frames_valid_default_request_time_range_stop_frame(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["time_range"]["stop_frame"] == 20

    def test_extract_frames_valid_default_request_time_range_stop_second(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["time_range"]["stop_second"] == 2.0

    def test_extract_frames_valid_default_request_image_format(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["image_format"] == "jpg"

    def test_extract_frames_valid_default_request_capture_rate(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["capture_rate"] == 1

    def test_extract_frames_valid_default_request_resize(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["resize"] == 1.0

    def test_extract_frames_valid_default_request_rotate(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["rotate"] == 0

    def test_extract_frames_valid_default_request_monochrome(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["monochrome"] is False

    def test_extract_frames_valid_default_request_dimensions(
        self, extracted_frames: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
    ):
        assert (
            extracted_frames["request"]["dimensions"] == video_properties["dimensions"]
        )

    def test_extract_frames_valid_default_request_images_expected(
        self, extracted_frames: t.Dict[str, t.Any]
    ):
        assert extracted_frames["request"]["images_expected"] == 20
