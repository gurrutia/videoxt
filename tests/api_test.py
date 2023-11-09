import shutil
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

from videoxt.api import (
    extract,
    extract_audio,
    extract_clip,
    extract_frames,
    extract_gif,
)
from videoxt.exceptions import InvalidExtractionMethod
from videoxt.result import Result


@pytest.fixture(scope="session")
def extract_frames_result(fixture_tmp_video_filepath) -> Generator[Result, None, None]:
    """Extract frames from a video and yield a Result object."""
    result = extract_frames(fixture_tmp_video_filepath)
    yield result
    try:
        shutil.rmtree(Path(result.destpath))
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session")
def generic_extract_frames_result(
    fixture_tmp_video_filepath,
) -> Generator[Result, None, None]:
    """Extract frames from a video using generic extract() and yield a Result object."""
    result = extract("frames", fixture_tmp_video_filepath, overwrite=True)
    yield result
    try:
        shutil.rmtree(Path(result.destpath))
    except FileNotFoundError:
        pass


def test_extract_frames_valid_default_request_success_is_true(
    extract_frames_result: Generator[Result, None, None],
    fixture_tmp_video_properties: dict[str, Any],
):
    """Test that the default request for extracting frames is successful."""
    assert extract_frames_result.success is True
    assert extract_frames_result.method == "frames"
    assert extract_frames_result.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent / "tmp.video.mp4_frames"
    )
    assert extract_frames_result.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_dir()


def test_generic_extract_frames_valid_default_request_success_is_true(
    generic_extract_frames_result: Generator[Result, None, None],
    fixture_tmp_video_properties: dict[str, Any],
):
    """Test that the default request for extracting frames is successful."""
    assert generic_extract_frames_result.success is True
    assert generic_extract_frames_result.method == "frames"
    assert generic_extract_frames_result.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent / "tmp.video.mp4_frames"
    )
    assert generic_extract_frames_result.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_dir()


@pytest.fixture(scope="session")
def extract_audio_result(fixture_tmp_video_filepath) -> Generator[Result, None, None]:
    """Extract audio from a video and yield a Result object."""
    result = extract_audio(fixture_tmp_video_filepath)
    yield result
    try:
        Path(result.destpath).unlink()
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session")
def generic_extract_audio_result(
    fixture_tmp_video_filepath,
) -> Generator[Result, None, None]:
    """Extract audio from a video using generic extract() and yield a Result object."""
    result = extract("audio", fixture_tmp_video_filepath, overwrite=True)
    yield result
    try:
        Path(result.destpath).unlink()
    except FileNotFoundError:
        pass


def test_extract_audio_valid_default_request_success_is_true(
    extract_audio_result: Generator[Result, None, None],
    fixture_tmp_video_properties: dict[str, Any],
):
    assert extract_audio_result.success is True
    assert extract_audio_result.method == "audio"
    assert extract_audio_result.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent / "tmp.video.mp3"
    )
    assert extract_audio_result.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_file()


def test_generic_extract_audio_valid_default_request_success_is_true(
    generic_extract_audio_result: Generator[Result, None, None],
    fixture_tmp_video_properties: dict[str, Any],
):
    assert generic_extract_audio_result.success is True
    assert generic_extract_audio_result.method == "audio"
    assert generic_extract_audio_result.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent / "tmp.video.mp3"
    )
    assert generic_extract_audio_result.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_file()


@pytest.fixture(scope="session")
def extract_clip_result(fixture_tmp_video_filepath) -> Generator[Result, None, None]:
    """Extract a clip from a video and yield a Result object."""
    result = extract_clip(fixture_tmp_video_filepath, filename="tmp.test.extract.clip")
    yield result
    try:
        Path(result.destpath).unlink()
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session")
def generic_extract_clip_result(
    fixture_tmp_video_filepath,
) -> Generator[Result, None, None]:
    """Extract a clip from a video using generic extract() and yield a Result object."""
    result = extract(
        "clip",
        fixture_tmp_video_filepath,
        filename="tmp.test.extract.clip",
        overwrite=True,
    )
    yield result
    try:
        Path(result.destpath).unlink()
    except FileNotFoundError:
        pass


def test_extract_clip_valid_default_request_success_is_true(
    extract_clip_result: Generator[Result, None, None],
    fixture_tmp_video_properties: dict[str, Any],
):
    assert extract_clip_result.success is True
    assert extract_clip_result.method == "clip"
    assert extract_clip_result.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent
        / "tmp.test.extract.clip.mp4"
    )
    assert extract_clip_result.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_file()


def test_generic_extract_clip_valid_default_request_success_is_true(
    generic_extract_clip_result: Generator[Result, None, None],
    fixture_tmp_video_properties: dict[str, Any],
):
    assert generic_extract_clip_result.success is True
    assert generic_extract_clip_result.method == "clip"
    assert generic_extract_clip_result.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent
        / "tmp.test.extract.clip.mp4"
    )
    assert generic_extract_clip_result.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_file()


@pytest.fixture(scope="session")
def extract_gif_result(fixture_tmp_video_filepath) -> Generator[Result, None, None]:
    """Extract a gif from a video and yield a Result object."""
    result = extract_gif(fixture_tmp_video_filepath)
    yield result
    try:
        Path(result.destpath).unlink()
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session")
def generic_extract_gif_result(
    fixture_tmp_video_filepath,
) -> Generator[Result, None, None]:
    """Extract a gif from a video using generic extract() and yield a Result object."""
    result = extract("gif", fixture_tmp_video_filepath, overwrite=True)
    yield result
    try:
        Path(result.destpath).unlink()
    except FileNotFoundError:
        pass


def test_extract_gif_valid_default_request_success_is_true(
    extract_gif_result: Generator[Result, None, None],
    fixture_tmp_video_properties: dict[str, Any],
):
    assert extract_gif_result.success is True
    assert extract_gif_result.method == "gif"
    assert extract_gif_result.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent / "tmp.video.gif"
    )
    assert extract_gif_result.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_file()


def test_generic_extract_gif_valid_default_request_success_is_true(
    generic_extract_gif_result: Generator[Result, None, None],
    fixture_tmp_video_properties: dict[str, Any],
):
    assert generic_extract_gif_result.success is True
    assert generic_extract_gif_result.method == "gif"
    assert generic_extract_gif_result.message == "Extraction successful."
    expected_destpath = (
        fixture_tmp_video_properties["video_file_path"].parent / "tmp.video.gif"
    )
    assert generic_extract_gif_result.destpath == expected_destpath
    expected_destpath = Path(expected_destpath)
    assert expected_destpath.exists()
    assert expected_destpath.is_file()


def test_extract_with_unsupported_extraction_method_raises_invalid_extraction_method_error(
    fixture_tmp_video_filepath,
):
    """Test that an invalid extraction method raises an InvalidExtractionMethodError."""
    with pytest.raises(InvalidExtractionMethod) as excinfo:
        extract("unsupported", fixture_tmp_video_filepath)
    assert "Invalid extraction method" in str(excinfo.value)
