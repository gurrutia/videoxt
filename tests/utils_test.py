import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pytest

from videoxt.utils import enumerate_dir
from videoxt.utils import enumerate_filepath
from videoxt.utils import parse_kwargs
from videoxt.utils import seconds_to_timestamp
from videoxt.utils import timestamp_to_seconds


def test_timestamp_to_seconds_valid_input():
    assert timestamp_to_seconds("1") == 1
    assert timestamp_to_seconds("1.1") == 1
    assert timestamp_to_seconds("59") == 59
    assert timestamp_to_seconds("60") == 60
    assert timestamp_to_seconds("0:00") == 0
    assert timestamp_to_seconds("1:01") == 61
    assert timestamp_to_seconds("1:01:01") == 3661
    assert timestamp_to_seconds("1:01:01.1") == 3661
    assert timestamp_to_seconds("1:01:01.1.1") == 3661


def test_timestamp_to_seconds_invalid_input():
    with pytest.raises(ValueError):
        timestamp_to_seconds("invalid")


def test_seconds_to_timestamp_valid_input():
    assert seconds_to_timestamp(-1) == "0:00:00"
    assert seconds_to_timestamp(0) == "0:00:00"
    assert seconds_to_timestamp(1) == "0:00:01"
    assert seconds_to_timestamp(59) == "0:00:59"
    assert seconds_to_timestamp(60) == "0:01:00"
    assert seconds_to_timestamp(61) == "0:01:01"
    assert seconds_to_timestamp(3661) == "1:01:01"
    assert seconds_to_timestamp(3661.1) == "1:01:01"


def test_seconds_to_timestamp_invalid_input():
    with pytest.raises(TypeError):
        seconds_to_timestamp("invalid")


@pytest.fixture
def temp_dir():
    temp_dir = Path("temp_dir")
    temp_dir.mkdir()
    yield temp_dir
    temp_dir.rmdir()


def test_enumerate_dir_existing_dir(temp_dir):
    # Test case 1: directory with same name already exists
    expected_output = temp_dir.with_name(f"{temp_dir.name} (2)")
    assert enumerate_dir(temp_dir) == expected_output


def test_enumerate_dir_new_dir(tmp_path):
    new_dir_path = tmp_path / "new_dir"
    assert enumerate_dir(new_dir_path) == new_dir_path


@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(b"test file contents")
    filepath = Path(tmp_file.name)
    yield filepath
    os.unlink(tmp_file.name)


def test_enumerate_filepath_existing_file(temp_file):
    # Test case 1: file with same name already exists
    expected_output = temp_file.with_name(f"{temp_file.stem} (2){temp_file.suffix}")
    assert enumerate_filepath(temp_file) == expected_output


def test_enumerate_filepath_new_file(temp_file):
    # Test case 2: file with same name does not exist
    new_filepath = temp_file.with_name("new_file.txt")
    assert enumerate_filepath(new_filepath) == new_filepath


@dataclass
class Image:
    width: int
    height: int


@dataclass
class Audio:
    artist: str
    title: str


def test_parse_kwargs_image():
    # Test case: parse kwargs for Image dataclass
    kwargs = {
        "filename": "my_image.jpg",
        "width": 1920,
        "height": 1080,
        "format": "jpg",
    }
    expected_output = {"width": 1920, "height": 1080}
    assert parse_kwargs(kwargs, Image) == expected_output


def test_parse_kwargs_audio():
    # Test case: parse kwargs for Audio dataclass
    kwargs = {
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "format": "mp3",
        "genre": "Rock",
    }
    expected_output = {"title": "Bohemian Rhapsody", "artist": "Queen"}
    assert parse_kwargs(kwargs, Audio) == expected_output
