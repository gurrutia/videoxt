import shutil
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

from videoxt.api import extract_audio, extract_clip, extract_frames, extract_gif
from videoxt.result import Result


@pytest.fixture(scope="session")
def extracted_frames(fixture_tmp_video_filepath) -> Generator[Result, None, None]:
    """Extract frames from a video and yield a Result object."""
    result = extract_frames(fixture_tmp_video_filepath)
    yield result
    if result.destpath is not None:
        shutil.rmtree(Path(result.destpath))


def test_extract_frames_valid_default_request_success_is_true(
    extracted_frames: Result, fixture_tmp_video_properties: dict[str, Any]
):
    assert extracted_frames.success is True
    assert extracted_frames.method == "frames"
    assert extracted_frames.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent / "tmp.video.mp4_frames"
    )
    assert extracted_frames.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_dir()


@pytest.fixture(scope="session")
def extracted_audio(fixture_tmp_video_filepath) -> Generator[Result, None, None]:
    """Extract audio from a video and yield a Result object."""
    result = extract_audio(fixture_tmp_video_filepath)
    yield result
    if result.destpath is not None:
        Path(result.destpath).unlink()


def test_extract_audio_valid_default_request_success_is_true(
    extracted_audio: Result, fixture_tmp_video_properties: dict[str, Any]
):
    assert extracted_audio.success is True
    assert extracted_audio.method == "audio"
    assert extracted_audio.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent / "tmp.video.mp3"
    )
    assert extracted_audio.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_file()


@pytest.fixture(scope="session")
def extracted_clip(fixture_tmp_video_filepath) -> Generator[Result, None, None]:
    """Extract a clip from a video and yield a Result object."""
    result = extract_clip(fixture_tmp_video_filepath, filename="tmp.test.extract.clip")
    yield result
    if result.destpath is not None:
        Path(result.destpath).unlink()


def test_extract_clip_valid_default_request_success_is_true(
    extracted_clip: Result, fixture_tmp_video_properties: dict[str, Any]
):
    assert extracted_clip.success is True
    assert extracted_clip.method == "clip"
    assert extracted_clip.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent
        / "tmp.test.extract.clip.mp4"
    )
    assert extracted_clip.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_file()


@pytest.fixture(scope="session")
def extracted_gif(fixture_tmp_video_filepath) -> Generator[Result, None, None]:
    """Extract a gif from a video and yield a Result object."""
    result = extract_gif(fixture_tmp_video_filepath)
    yield result
    if result.destpath is not None:
        Path(result.destpath).unlink()


def test_extract_gif_valid_default_request_success_is_true(
    extracted_gif: Result, fixture_tmp_video_properties: dict[str, Any]
):
    assert extracted_gif.success is True
    assert extracted_gif.method == "gif"
    assert extracted_gif.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent / "tmp.video.gif"
    )
    assert extracted_gif.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_file()
