import shutil
import typing as t
from pathlib import Path

import pytest

from videoxt.utils import parse_kwargs
from videoxt.video import VideoProperties


@pytest.fixture(scope="session")
def extracted_frames(tmp_video_filepath: Path) -> t.Dict[str, t.Any]:
    """Extract frames from a video and yield the directory where they were saved.

    Yields:
        Path: The directory where the frames were saved.
    """
    from videoxt.api import extract_frames

    results = extract_frames(tmp_video_filepath)
    yield results
    shutil.rmtree(results["request"]["destdir"])


def test_extract_frames_valid_default_request_success_is_true(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["success"] is True


def test_extract_frames_valid_default_request_video_filepath(
    extracted_frames: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert (
        extracted_frames["request"]["video"]["filepath"]
        == video_properties["video_file_path"]
    )


def test_extract_frames_valid_default_request_video_properties(
    extracted_frames: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    expected_properties = parse_kwargs(video_properties, VideoProperties)
    assert extracted_frames["request"]["video"]["properties"] == expected_properties


def test_extract_frames_valid_default_request_start_time(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["start_time"] == "0:00:00"


def test_extract_frames_valid_default_request_stop_time(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["stop_time"] is None


def test_extract_frames_valid_default_request_fps(
    extracted_frames: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["fps"] == video_properties["fps"]


def test_extract_frames_valid_default_request_destdir_exists(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["destdir"].exists()


def test_extract_frames_valid_default_request_filename(
    extracted_frames: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["filename"] == video_properties["filename"]


def test_extract_frames_valid_default_request_verbose(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["verbose"] is False


def test_extract_frames_valid_default_request_time_range_start_timestamp(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["time_range"]["start_timestamp"] == "0:00:00"


def test_extract_frames_valid_default_request_time_range_start_frame(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["time_range"]["start_frame"] == 0


def test_extract_frames_valid_default_request_time_range_start_second(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["time_range"]["start_second"] == 0.0


def test_extract_frames_valid_default_request_time_range_stop_timestamp(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["time_range"]["stop_timestamp"] == "0:00:02"


def test_extract_frames_valid_default_request_time_range_stop_frame(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["time_range"]["stop_frame"] == 20


def test_extract_frames_valid_default_request_time_range_stop_second(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["time_range"]["stop_second"] == 2.0


def test_extract_frames_valid_default_request_image_format(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["image_format"] == "jpg"


def test_extract_frames_valid_default_request_capture_rate(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["capture_rate"] == 1


def test_extract_frames_valid_default_request_resize(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["resize"] == 1.0


def test_extract_frames_valid_default_request_rotate(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["rotate"] == 0


def test_extract_frames_valid_default_request_monochrome(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["monochrome"] is False


def test_extract_frames_valid_default_request_dimensions(
    extracted_frames: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["dimensions"] == video_properties["dimensions"]


def test_extract_frames_valid_default_request_images_expected(
    extracted_frames: t.Dict[str, t.Any]
):
    assert extracted_frames["request"]["images_expected"] == 20


@pytest.fixture(scope="session")
def extracted_audio(tmp_video_filepath: Path) -> t.Dict[str, t.Any]:
    """Extract audio from a video and yield the filepath where it was saved.

    Yields:
        Path: The filepath where the audio was saved.
    """
    from videoxt.api import extract_audio

    results = extract_audio(tmp_video_filepath)
    yield results
    results["request"]["filepath"].unlink()


def test_extract_audio_valid_default_request_success_is_true(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["success"] is True


def test_extract_audio_valid_default_request_video_filepath(
    extracted_audio: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert (
        extracted_audio["request"]["video"]["filepath"]
        == video_properties["video_file_path"]
    )


def test_extract_audio_valid_default_request_video_properties(
    extracted_audio: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    expected_properties = parse_kwargs(video_properties, VideoProperties)
    assert extracted_audio["request"]["video"]["properties"] == expected_properties


def test_extract_audio_valid_default_request_start_time(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["start_time"] == "0:00:00"


def test_extract_audio_valid_default_request_stop_time(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["stop_time"] is None


def test_extract_audio_valid_default_request_fps(
    extracted_audio: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["fps"] == video_properties["fps"]


def test_extract_audio_valid_default_request_destdir_exists(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["destdir"].exists()


def test_extract_audio_valid_default_request_filename(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["filename"] is None


def test_extract_audio_valid_default_request_verbose(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["verbose"] is False


def test_extract_audio_valid_default_request_time_range_start_timestamp(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["time_range"]["start_timestamp"] == "0:00:00"


def test_extract_audio_valid_default_request_time_range_start_frame(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["time_range"]["start_frame"] == 0


def test_extract_audio_valid_default_request_time_range_start_second(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["time_range"]["start_second"] == 0.0


def test_extract_audio_valid_default_request_time_range_stop_timestamp(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["time_range"]["stop_timestamp"] == "0:00:02"


def test_extract_audio_valid_default_request_time_range_stop_frame(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["time_range"]["stop_frame"] == 20


def test_extract_audio_valid_default_request_time_range_stop_second(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["time_range"]["stop_second"] == 2.0


def test_extract_audio_valid_default_request_audio_format(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["audio_format"] == "mp3"


def test_extract_audio_valid_default_request_speed(extracted_audio: t.Dict[str, t.Any]):
    assert extracted_audio["request"]["speed"] == 1.0


def test_extract_audio_valid_default_request_volume(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["volume"] == 1.0


def test_extract_audio_valid_default_request_bounce(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["bounce"] is False


def test_extract_audio_valid_default_request_reverse(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["reverse"] is False


def test_extract_audio_valid_default_request_normalize(
    extracted_audio: t.Dict[str, t.Any]
):
    assert extracted_audio["request"]["normalize"] is False


@pytest.fixture(scope="session")
def extracted_clip(tmp_video_filepath: Path) -> t.Dict[str, t.Any]:
    """Extract a clip from a video and yield the filepath where it was saved.

    Yields:
        Path: The filepath where the clip was saved.
    """
    from videoxt.api import extract_clip

    results = extract_clip(tmp_video_filepath)
    yield results
    results["request"]["filepath"].unlink()


def test_extract_clip_valid_default_request_success_is_true(
    extracted_clip: t.Dict[str, t.Any]
):
    assert extracted_clip["success"] is True


def test_extract_clip_valid_default_request_video_filepath(
    extracted_clip: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert (
        extracted_clip["request"]["video"]["filepath"]
        == video_properties["video_file_path"]
    )


def test_extract_clip_valid_default_request_video_properties(
    extracted_clip: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    expected_properties = parse_kwargs(video_properties, VideoProperties)
    assert extracted_clip["request"]["video"]["properties"] == expected_properties


def test_extract_clip_valid_default_request_start_time(
    extracted_clip: t.Dict[str, t.Any]
):
    assert extracted_clip["request"]["start_time"] == "0:00:00"


def test_extract_clip_valid_default_request_stop_time(
    extracted_clip: t.Dict[str, t.Any]
):
    assert extracted_clip["request"]["stop_time"] is None


def test_extract_clip_valid_default_request_fps(
    extracted_clip: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert extracted_clip["request"]["fps"] == video_properties["fps"]


def test_extract_clip_valid_default_request_destdir_exists(
    extracted_clip: t.Dict[str, t.Any]
):
    assert extracted_clip["request"]["destdir"].exists()


def test_extract_clip_valid_default_request_filename(
    extracted_clip: t.Dict[str, t.Any]
):
    assert extracted_clip["request"]["filename"] is None


def test_extract_clip_valid_default_request_verbose(extracted_clip: t.Dict[str, t.Any]):
    assert extracted_clip["request"]["verbose"] is False


def test_extract_clip_valid_default_request_resize(extracted_clip: t.Dict[str, t.Any]):
    assert extracted_clip["request"]["resize"] == 1.0


def test_extract_clip_valid_default_request_rotate(extracted_clip: t.Dict[str, t.Any]):
    assert extracted_clip["request"]["rotate"] == 0


def test_extract_clip_valid_default_request_monochrome(
    extracted_clip: t.Dict[str, t.Any]
):
    assert extracted_clip["request"]["monochrome"] is False


def test_extract_clip_valid_default_request_dimensions(
    extracted_clip: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert extracted_clip["request"]["dimensions"] == video_properties["dimensions"]


def test_extract_clip_valid_default_request_speed(extracted_clip: t.Dict[str, t.Any]):
    assert extracted_clip["request"]["speed"] == 1.0


def test_extract_clip_valid_default_request_volume(extracted_clip: t.Dict[str, t.Any]):
    assert extracted_clip["request"]["volume"] == 1.0


def test_extract_clip_valid_default_request_bounce(extracted_clip: t.Dict[str, t.Any]):
    assert extracted_clip["request"]["bounce"] is False


def test_extract_clip_valid_default_request_reverse(extracted_clip: t.Dict[str, t.Any]):
    assert extracted_clip["request"]["reverse"] is False


def test_extract_clip_valid_default_request_normalize(
    extracted_clip: t.Dict[str, t.Any]
):
    assert extracted_clip["request"]["normalize"] is False


@pytest.fixture(scope="session")
def extracted_gif(tmp_video_filepath: Path) -> t.Dict[str, t.Any]:
    """Extract a gif from a video and yield the filepath where it was saved.

    Yields:
        Path: The filepath where the gif was saved.
    """
    from videoxt.api import extract_gif

    results = extract_gif(tmp_video_filepath)
    yield results
    results["request"]["filepath"].unlink()


def test_extract_gif_valid_default_request_success_is_true(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["success"] is True


def test_extract_gif_valid_default_request_video_filepath(
    extracted_gif: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert (
        extracted_gif["request"]["video"]["filepath"]
        == video_properties["video_file_path"]
    )


def test_extract_gif_valid_default_request_video_properties(
    extracted_gif: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    expected_properties = parse_kwargs(video_properties, VideoProperties)
    assert extracted_gif["request"]["video"]["properties"] == expected_properties


def test_extract_gif_valid_default_request_start_time(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["start_time"] == "0:00:00"


def test_extract_gif_valid_default_request_stop_time(extracted_gif: t.Dict[str, t.Any]):
    assert extracted_gif["request"]["stop_time"] is None


def test_extract_gif_valid_default_request_fps(
    extracted_gif: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["fps"] == video_properties["fps"]


def test_extract_gif_valid_default_request_destdir_exists(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["destdir"].exists()


def test_extract_gif_valid_default_request_filename(extracted_gif: t.Dict[str, t.Any]):
    assert extracted_gif["request"]["filename"] is None


def test_extract_gif_valid_default_request_verbose(extracted_gif: t.Dict[str, t.Any]):
    assert extracted_gif["request"]["verbose"] is False


def test_extract_gif_valid_default_request_resize(extracted_gif: t.Dict[str, t.Any]):
    assert extracted_gif["request"]["resize"] == 1.0


def test_extract_gif_valid_default_request_rotate(extracted_gif: t.Dict[str, t.Any]):
    assert extracted_gif["request"]["rotate"] == 0


def test_extract_gif_valid_default_request_speed(extracted_gif: t.Dict[str, t.Any]):
    assert extracted_gif["request"]["speed"] == 1.0


def test_extract_gif_valid_default_request_time_range_start_timestamp(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["time_range"]["start_timestamp"] == "0:00:00"


def test_extract_gif_valid_default_request_time_range_start_frame(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["time_range"]["start_frame"] == 0


def test_extract_gif_valid_default_request_time_range_start_second(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["time_range"]["start_second"] == 0.0


def test_extract_gif_valid_default_request_time_range_stop_timestamp(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["time_range"]["stop_timestamp"] == "0:00:02"


def test_extract_gif_valid_default_request_time_range_stop_frame(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["time_range"]["stop_frame"] == 20


def test_extract_gif_valid_default_request_time_range_stop_second(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["time_range"]["stop_second"] == 2.0


def test_extract_gif_valid_default_request_dimensions(
    extracted_gif: t.Dict[str, t.Any], video_properties: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["dimensions"] == video_properties["dimensions"]


def test_extract_gif_valid_default_request_monochrome(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["monochrome"] is False


def test_extract_gif_valid_default_request_file_is_gif(
    extracted_gif: t.Dict[str, t.Any]
):
    assert extracted_gif["request"]["filepath"].suffix == ".gif"
