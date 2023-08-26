from dataclasses import dataclass
from pathlib import Path

import pytest

from videoxt.utils import enumerate_dir
from videoxt.utils import enumerate_filepath
from videoxt.utils import parse_kwargs
from videoxt.utils import seconds_to_timestamp
from videoxt.utils import timestamp_to_seconds


def test_timestamp_to_seconds_valid_input():
    """Test that the function returns a valid number of seconds for a given timestamp."""
    assert timestamp_to_seconds("0:00") == 0
    assert timestamp_to_seconds("0:01") == 1
    assert timestamp_to_seconds("0:59") == 59
    assert timestamp_to_seconds("1:00") == 60
    assert timestamp_to_seconds("1:01") == 61
    assert timestamp_to_seconds("0:00:00") == 0
    assert timestamp_to_seconds("0:00:01") == 1
    assert timestamp_to_seconds("0:00:59") == 59
    assert timestamp_to_seconds("0:01:00") == 60
    assert timestamp_to_seconds("0:01:01") == 61
    assert timestamp_to_seconds("1:00:00") == 3600
    assert timestamp_to_seconds("1:00:01") == 3601
    assert timestamp_to_seconds("1:00:59") == 3659
    assert timestamp_to_seconds("1:01:00") == 3660
    assert timestamp_to_seconds("1:01:01") == 3661


def test_timestamp_to_seconds_abnormal_but_valid_input():
    """Test that the function returns a valid number of seconds for an abnormal timestamp.

    The following timestamps are not valid according to the function's docstring, but they should
    be treated be handled by the function.
    """
    assert timestamp_to_seconds("0") == 0
    assert timestamp_to_seconds("1") == 1
    assert timestamp_to_seconds("1.1") == 1
    assert timestamp_to_seconds("1.1.1") == 1
    assert timestamp_to_seconds("59") == 59
    assert timestamp_to_seconds("60") == 60
    assert timestamp_to_seconds("61") == 61
    assert timestamp_to_seconds("61.1") == 61
    assert timestamp_to_seconds("61.1.1") == 61
    assert timestamp_to_seconds("1:01.1") == 61
    assert timestamp_to_seconds("1:01.1.1") == 61
    assert timestamp_to_seconds("0:01:01.1") == 61
    assert timestamp_to_seconds("0:01:01.1.1") == 61
    assert timestamp_to_seconds("1:01:01.1") == 3661
    assert timestamp_to_seconds("1:01:01.1.1") == 3661
    assert timestamp_to_seconds("1:1") == 61
    assert timestamp_to_seconds("1:1:1") == 3661
    assert timestamp_to_seconds("1:1:1.1") == 3661
    assert timestamp_to_seconds("1:1:1.1.1") == 3661


def test_timestamp_to_seconds_invalid_input():
    """Test that the function raises a ValueError if the input is not a valid timestamp."""
    with pytest.raises(ValueError):
        timestamp_to_seconds("invalid")


def test_timestamp_to_seconds_empty_string():
    """Test that the function raises a ValueError if the input is an empty string."""
    with pytest.raises(ValueError):
        timestamp_to_seconds("")


def test_seconds_to_timestamp_valid_input():
    """Test that the function returns a valid timestamp string for a given number of seconds."""
    assert seconds_to_timestamp(-1) == "0:00:00"
    assert seconds_to_timestamp(0) == "0:00:00"
    assert seconds_to_timestamp(0.0) == "0:00:00"
    assert seconds_to_timestamp(0.001) == "0:00:00"
    assert seconds_to_timestamp(0.999) == "0:00:00"
    assert seconds_to_timestamp(1) == "0:00:01"
    assert seconds_to_timestamp(1.0) == "0:00:01"
    assert seconds_to_timestamp(1.001) == "0:00:01"
    assert seconds_to_timestamp(1.999) == "0:00:01"
    assert seconds_to_timestamp(59) == "0:00:59"
    assert seconds_to_timestamp(59.0) == "0:00:59"
    assert seconds_to_timestamp(59.001) == "0:00:59"
    assert seconds_to_timestamp(59.999) == "0:00:59"
    assert seconds_to_timestamp(60) == "0:01:00"
    assert seconds_to_timestamp(60.0) == "0:01:00"
    assert seconds_to_timestamp(60.001) == "0:01:00"
    assert seconds_to_timestamp(60.999) == "0:01:00"
    assert seconds_to_timestamp(61) == "0:01:01"
    assert seconds_to_timestamp(61.0) == "0:01:01"
    assert seconds_to_timestamp(61.001) == "0:01:01"
    assert seconds_to_timestamp(61.999) == "0:01:01"
    assert seconds_to_timestamp(3600) == "1:00:00"
    assert seconds_to_timestamp(3600.0) == "1:00:00"
    assert seconds_to_timestamp(3600.001) == "1:00:00"
    assert seconds_to_timestamp(3600.999) == "1:00:00"
    assert seconds_to_timestamp(3601) == "1:00:01"
    assert seconds_to_timestamp(3601.0) == "1:00:01"
    assert seconds_to_timestamp(3601.001) == "1:00:01"
    assert seconds_to_timestamp(3601.999) == "1:00:01"
    assert seconds_to_timestamp(3659) == "1:00:59"
    assert seconds_to_timestamp(3659.0) == "1:00:59"
    assert seconds_to_timestamp(3659.001) == "1:00:59"
    assert seconds_to_timestamp(3659.999) == "1:00:59"
    assert seconds_to_timestamp(3661) == "1:01:01"
    assert seconds_to_timestamp(3661.0) == "1:01:01"
    assert seconds_to_timestamp(3661.001) == "1:01:01"
    assert seconds_to_timestamp(3661.999) == "1:01:01"


def test_seconds_to_timestamp_invalid_input():
    """Test that the function raises a TypeError if the input is not a numeric value."""
    with pytest.raises(TypeError):
        seconds_to_timestamp("invalid")


def test_seconds_to_timestamp_empty_string():
    """Test that the function raises a ValueError if the input is an empty string."""
    with pytest.raises(TypeError):
        seconds_to_timestamp("")


def test_enumerate_dir_existing_dir(tmp_path: Path):
    """Test that the directory path is enumerated if the directory already exists.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    expected_path = tmp_path.with_name(f"{tmp_path.name} (2)")
    assert enumerate_dir(tmp_path) == expected_path


def test_enumerate_dir_new_dir(tmp_path: Path):
    """Test that the same directory path is returned if the directory does not exist.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    expected_path = tmp_path / "new_dir"
    assert enumerate_dir(expected_path) == expected_path


def test_enumerate_filepath_existing_file(tmp_text_filepath: Path):
    """Test that the filepath is enumerated if the file already exists.

    `tmp_text_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    expected_path = tmp_text_filepath.with_name(
        f"{tmp_text_filepath.stem} (2){tmp_text_filepath.suffix}"
    )
    assert enumerate_filepath(tmp_text_filepath) == expected_path


def test_enumerate_filepath_new_file(tmp_text_filepath: Path):
    """Test that the same filepath is returned if the file does not exist.

    `tmp_text_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    expected_path = tmp_text_filepath.with_name("new_file.txt")
    assert enumerate_filepath(expected_path) == expected_path


@dataclass
class Image:
    """Test dataclass for the `utils.parse_kwargs` function."""

    filename: str
    width: int
    height: int


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        # Test case 1: all kwargs are defined as fields in the `Image` dataclass.
        (
            {
                "filename": "image.jpg",
                "width": 1920,
                "height": 1080,
            },
            {"filename": "image.jpg", "width": 1920, "height": 1080},
        ),
        # Test case 2: all kwargs are defined as fields in the `Image` dataclass except `extra_field`.
        (
            {
                "filename": "image.jpg",
                "width": 1920,
                "height": 1080,
                "extra_field": "",
            },
            {"filename": "image.jpg", "width": 1920, "height": 1080},
        ),
        # Test case 3: select kwargs are defined as fields in the `Image` dataclass.
        (
            {"width": 1920, "height": 1080},
            {"width": 1920, "height": 1080},
        ),
        # Test case 4: one of two kwargs are defined as fields in the `Image` dataclass.
        (
            {"filename": "image.jpg", "extra_field": ""},
            {"filename": "image.jpg"},
        ),
        # Test case 5: one of one kwarg is defined as a field in the `Image` dataclass.
        (
            {"filename": "image.jpg"},
            {"filename": "image.jpg"},
        ),
        # Test case 6: no kwargs are defined as fields in the `Image` dataclass.
        (
            {"extra_field": "", "another_extra_field": ""},
            {},
        ),
        # Test case 7: one of one kwarg is not defined as a field in the `Image` dataclass.
        (
            {"extra_field": ""},
            {},
        ),
        # Test case 8: empty kwargs passed.
        (
            {},
            {},
        ),
        # Test case 9: all kwargs are defined as fields in the `Image` dataclass, but one is None.
        (
            {
                "filename": "image.jpg",
                "width": 1920,
                "height": None,
            },
            {"filename": "image.jpg", "width": 1920, "height": None},
        ),
    ],
)
def test_parse_kwargs(kwargs: dict, expected: dict):
    """Test that the `parse_kwargs` function returns a dictonary containing only the
    keyword arguments that match the fields in a given dataclass."""
    assert parse_kwargs(kwargs, Image) == expected
