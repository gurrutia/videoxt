import os
from argparse import ArgumentTypeError
from pathlib import Path

import pytest

import videoxt.constants as C
from videoxt.validators import _raise_error
from videoxt.validators import non_negative_float
from videoxt.validators import non_negative_int
from videoxt.validators import positive_float
from videoxt.validators import positive_int
from videoxt.validators import valid_capture_rate
from videoxt.validators import valid_dimensions
from videoxt.validators import valid_dir
from videoxt.validators import valid_extraction_range
from videoxt.validators import valid_filename
from videoxt.validators import valid_filepath
from videoxt.validators import valid_image_format
from videoxt.validators import valid_resize_value
from videoxt.validators import valid_rotate_value
from videoxt.validators import valid_start_time
from videoxt.validators import valid_stop_time
from videoxt.validators import valid_timestamp
from videoxt.validators import valid_video_filepath
from videoxt.validators import ValidationException


def test_positive_int_valid_int():
    assert positive_int(42, from_cli=False) == 42
    assert positive_int(42, from_cli=True) == 42


def test_positive_int_valid_string():
    assert positive_int("42", from_cli=False) == 42
    assert positive_int("42", from_cli=True) == 42


def test_positive_int_valid_float():
    assert positive_int(42.0, from_cli=False) == 42
    assert positive_int(42.0, from_cli=True) == 42


def test_positive_int_valid_float_string():
    assert positive_int("42.0", from_cli=False) == 42
    assert positive_int("42.0", from_cli=True) == 42


def test_positive_int_zero_int():
    with pytest.raises(ValidationException):
        positive_int(0, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int(0, from_cli=True)


def test_positive_int_zero_int_string():
    with pytest.raises(ValidationException):
        positive_int("0", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int("0", from_cli=True)


def test_positive_int_zero_float():
    with pytest.raises(ValidationException):
        positive_int(0.0, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int(0.0, from_cli=True)


def test_positive_int_negative_int():
    with pytest.raises(ValidationException):
        positive_int(-42, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int(-42, from_cli=True)


def test_positive_int_negative_int_string():
    with pytest.raises(ValidationException):
        positive_int("-42", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int("-42", from_cli=True)


def test_positive_int_negative_float():
    with pytest.raises(ValidationException):
        positive_int(-42.0, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int(-42.0, from_cli=True)


def test_positive_int_negative_float_string():
    with pytest.raises(ValidationException):
        positive_int("-42.0", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int("-42.0", from_cli=True)


def test_positive_int_invalid_float():
    with pytest.raises(ValidationException):
        positive_int(42.5, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int(42.5, from_cli=True)


def test_positive_int_invalid_float_string():
    with pytest.raises(ValidationException):
        positive_int("42.5", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int("42.5", from_cli=True)


def test_positive_int_invalid_string():
    with pytest.raises(ValidationException):
        positive_int("abc", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int("abc", from_cli=True)


def test_positive_int_empty_string():
    with pytest.raises(ValidationException):
        positive_int("", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int("", from_cli=True)


def test_positive_int_none():
    with pytest.raises(ValidationException):
        positive_int(None, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int(None, from_cli=True)


def test_positive_int_invalid_string():
    with pytest.raises(ValidationException):
        positive_int("abc", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_int("abc", from_cli=True)


def test_positive_float_valid_float():
    assert positive_float(3.14, from_cli=False) == 3.14
    assert positive_float(3.14, from_cli=True) == 3.14


def test_positive_float_valid_float_string():
    assert positive_float("3.14", from_cli=False) == 3.14
    assert positive_float("3.14", from_cli=True) == 3.14


def test_positive_float_valid_int():
    assert positive_float(42, from_cli=False) == 42.0
    assert positive_float(42, from_cli=True) == 42.0


def test_positive_float_valid_int_string():
    assert positive_float("42", from_cli=False) == 42.0
    assert positive_float("42", from_cli=True) == 42.0


def test_positive_float_negative_float():
    with pytest.raises(ValidationException):
        positive_float(-3.14, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float(-3.14, from_cli=True)


def test_positive_float_negative_float_string():
    with pytest.raises(ValidationException):
        positive_float("-3.14", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float("-3.14", from_cli=True)


def test_positive_float_negative_int():
    with pytest.raises(ValidationException):
        positive_float(-42, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float(-42, from_cli=True)


def test_positive_float_negative_int_string():
    with pytest.raises(ValidationException):
        positive_float("-42", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float("-42", from_cli=True)


def test_positive_float_zero_float():
    with pytest.raises(ValidationException):
        positive_float(0.0, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float(0.0, from_cli=True)


def test_positive_float_zero_float_string():
    with pytest.raises(ValidationException):
        positive_float("0.0", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float("0.0", from_cli=True)


def test_positive_float_zero_int():
    with pytest.raises(ValidationException):
        positive_float(0, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float(0, from_cli=True)


def test_positive_float_zero_int_string():
    with pytest.raises(ValidationException):
        positive_float("0", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float("0", from_cli=True)


def test_positive_float_invalid_string():
    with pytest.raises(ValidationException):
        positive_float("abc", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float("abc", from_cli=True)


def test_positive_float_empty_string():
    with pytest.raises(ValidationException):
        positive_float("", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float("", from_cli=True)


def test_positive_float_none():
    with pytest.raises(ValidationException):
        positive_float(None, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        positive_float(None, from_cli=True)


def test_non_negative_int_valid():
    assert non_negative_int(42, from_cli=False) == 42
    assert non_negative_int(42, from_cli=True) == 42


def test_non_negative_int_valid_string():
    assert non_negative_int("42", from_cli=False) == 42
    assert non_negative_int("42", from_cli=True) == 42


def test_non_negative_int_valid_float():
    assert non_negative_int(42.0, from_cli=False) == 42
    assert non_negative_int(42.0, from_cli=True) == 42


def test_non_negative_int_valid_float_string():
    assert non_negative_int("42.0", from_cli=False) == 42
    assert non_negative_int("42.0", from_cli=True) == 42


def test_non_negative_int_zero_int():
    assert non_negative_int(0, from_cli=False) == 0
    assert non_negative_int(0, from_cli=True) == 0


def test_non_negative_int_zero_int_string():
    assert non_negative_int("0", from_cli=False) == 0
    assert non_negative_int("0", from_cli=True) == 0


def test_non_negative_int_zero_float():
    assert non_negative_int(0.0, from_cli=False) == 0
    assert non_negative_int(0.0, from_cli=True) == 0


def test_non_negative_int_negative_int():
    with pytest.raises(ValidationException):
        non_negative_int(-42, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_int(-42, from_cli=True)


def test_non_negative_int_negative_int_string():
    with pytest.raises(ValidationException):
        non_negative_int("-42", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_int("-42", from_cli=True)


def test_non_negative_int_negative_float():
    with pytest.raises(ValidationException):
        non_negative_int(-42.0, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_int(-42.0, from_cli=True)


def test_non_negative_int_negative_float_string():
    with pytest.raises(ValidationException):
        non_negative_int("-42.0", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_int("-42.0", from_cli=True)


def test_non_negative_int_invalid_float():
    with pytest.raises(ValidationException):
        non_negative_int(42.5, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_int(42.5, from_cli=True)


def test_non_negative_int_invalid_float_string():
    with pytest.raises(ValidationException):
        non_negative_int("42.5", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_int("42.5", from_cli=True)


def test_non_negative_int_invalid_string():
    with pytest.raises(ValidationException):
        non_negative_int("abc", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_int("abc", from_cli=True)


def test_non_negative_int_empty_string():
    with pytest.raises(ValidationException):
        non_negative_int("", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_int("", from_cli=True)


def test_non_negative_int_none():
    with pytest.raises(ValidationException):
        non_negative_int(None, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_int(None, from_cli=True)


def test_non_negative_float_valid_float():
    assert non_negative_float(3.14, from_cli=False) == 3.14
    assert non_negative_float(3.14, from_cli=True) == 3.14


def test_non_negative_float_valid_float_string():
    assert non_negative_float("3.14", from_cli=False) == 3.14
    assert non_negative_float("3.14", from_cli=True) == 3.14


def test_non_negative_float_valid_int():
    assert non_negative_float(42, from_cli=False) == 42.0
    assert non_negative_float(42, from_cli=True) == 42.0


def test_non_negative_float_valid_int_string():
    assert non_negative_float("42", from_cli=False) == 42.0
    assert non_negative_float("42", from_cli=True) == 42.0


def test_non_negative_float_zero_float():
    assert non_negative_float(0.0, from_cli=False) == 0.0
    assert non_negative_float(0.0, from_cli=True) == 0.0


def test_non_negative_float_zero_float_string():
    assert non_negative_float("0.0", from_cli=False) == 0.0
    assert non_negative_float("0.0", from_cli=True) == 0.0


def test_non_negative_float_zero_int():
    assert non_negative_float(0, from_cli=False) == 0.0
    assert non_negative_float(0, from_cli=True) == 0.0


def test_non_negative_float_zero_int_string():
    assert non_negative_float("0", from_cli=False) == 0.0
    assert non_negative_float("0", from_cli=True) == 0.0


def test_non_negative_float_negative_float():
    with pytest.raises(ValidationException):
        non_negative_float(-3.14, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_float(-3.14, from_cli=True)


def test_non_negative_float_negative_float_string():
    with pytest.raises(ValidationException):
        non_negative_float("-3.14", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_float("-3.14", from_cli=True)


def test_non_negative_float_negative_int():
    with pytest.raises(ValidationException):
        non_negative_float(-42, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_float(-42, from_cli=True)


def test_non_negative_float_negative_int_string():
    with pytest.raises(ValidationException):
        non_negative_float("-42", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_float("-42", from_cli=True)


def test_non_negative_float_invalid_string():
    with pytest.raises(ValidationException):
        non_negative_float("abc", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_float("abc", from_cli=True)


def test_non_negative_float_empty_string():
    with pytest.raises(ValidationException):
        non_negative_float("", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_float("", from_cli=True)


def test_non_negative_float_none():
    with pytest.raises(ValidationException):
        non_negative_float(None, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        non_negative_float(None, from_cli=True)


def test_valid_filepath_valid_path(tmp_video_filepath: Path):
    """Test that a valid filepath is returned when a valid pathlib path is passed.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    assert valid_filepath(tmp_video_filepath, from_cli=False) == tmp_video_filepath
    assert valid_filepath(tmp_video_filepath, from_cli=True) == tmp_video_filepath


def test_valid_filepath_valid_string(tmp_video_filepath: Path):
    """Test that a valid filepath is returned when a valid string filepath is passed.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    assert valid_filepath(str(tmp_video_filepath), from_cli=False) == tmp_video_filepath
    assert valid_filepath(str(tmp_video_filepath), from_cli=True) == tmp_video_filepath


def test_valid_filepath_nonexistent_path():
    path = Path("nonexistent") / "file.mp4"
    with pytest.raises(ValidationException):
        valid_filepath(path, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_filepath(path, from_cli=True)


def test_valid_filepath_nonexistent_string():
    path = "nonexistent/file.mp4"
    with pytest.raises(ValidationException):
        valid_filepath(path, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_filepath(path, from_cli=True)


def test_valid_filepath_none():
    with pytest.raises(ValidationException):
        valid_filepath(None, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_filepath(None, from_cli=True)


def test_valid_dir_valid_path(tmp_path: Path):
    """Test that a valid directory is returned when a valid pathlib directory is passed.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    assert valid_dir(tmp_path, from_cli=False) == tmp_path
    assert valid_dir(tmp_path, from_cli=True) == tmp_path


def test_valid_dir_valid_string(tmp_path: Path):
    """Test that a valid directory is returned when a valid string directory is passed.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    assert valid_dir(str(tmp_path), from_cli=False) == tmp_path
    assert valid_dir(str(tmp_path), from_cli=True) == tmp_path


def test_valid_dir_invalid_path(tmp_path: Path):
    """When a nonexistent pathlib directory is passed, test that a ValidationException is raised
    when from_cli is False and an ArgumentTypeError is raised when from_cli is True.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    with pytest.raises(ValidationException):
        valid_dir(tmp_path / "invalid", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_dir(tmp_path / "invalid", from_cli=True)


def test_valid_dir_invalid_string(tmp_path: Path):
    """When a nonexistent string directory is passed, test that a ValidationException is raised
    when from_cli is False and an ArgumentTypeError is raised when from_cli is True.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    with pytest.raises(ValidationException):
        valid_dir(str(tmp_path / "invalid"), from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_dir(str(tmp_path / "invalid"), from_cli=True)


def test_valid_dir_none():
    """Test that a ValidationException is raised when None is passed."""
    with pytest.raises(ValidationException):
        valid_dir(None, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_dir(None, from_cli=True)


@pytest.mark.parametrize(
    ("start", "stop", "duration", "expected"),
    [
        (0, 1, 2, True),  # start < stop < duration
        (1, 3, 3, True),  # stop < stop, stop == duration
    ],
)
def test_valid_extraction_range_valid_range(
    start: float, stop: float, duration: float, expected: bool
):
    assert valid_extraction_range(start, stop, duration) == expected


@pytest.mark.parametrize(
    ("start", "stop", "duration"),
    [
        (1, 0, 0),  # start > duration
        (1, 1, 2),  # start == stop
        (1, 0, 2),  # start > stop
    ],
)
def test_valid_extraction_range_invalid_range(
    start: float, stop: float, duration: float
):
    with pytest.raises(ValidationException):
        valid_extraction_range(start, stop, duration)


@pytest.mark.parametrize(
    ("filename", "expected_filename"),
    [
        ("filename", "filename"),
        ("filename (1)", "filename (1)"),
        ("filename-with-dashes", "filename-with-dashes"),
        ("filename with spaces", "filename with spaces"),
        ("filename_with_underscores", "filename_with_underscores"),
        ("filenamewithsuffix.mp4", "filenamewithsuffix.mp4"),
        ("filenameendswithdot.", "filenameendswithdot."),
        (".filenamestartswithdot", ".filenamestartswithdot"),
        (" filename starts with space", " filename starts with space"),
        ("filename ends with space ", "filename ends with space "),
        (
            "filename_with_symbols!@#$%^&()_+{}[];'",
            "filename_with_symbols!@#$%^&()_+{}[];'",
        ),
        (".mp4.", ".mp4."),
        (".mp4", ".mp4"),
        (".", "."),
        (" ", " "),
    ],
)
def test_valid_filename_valid_filenames(filename: str, expected_filename: str):
    assert valid_filename(filename, from_cli=False) == expected_filename
    assert valid_filename(filename, from_cli=True) == expected_filename


@pytest.mark.parametrize(
    ("filename"),
    [
        ("file|with|invalid|characters.mp4"),
        ("file\\\\with\\\\backslashes.mp4"),
        ("file/with/forward/slashes.mp4"),
        ("file*with*asterisks.mp4"),
        ("file?with?question?marks.mp4"),
        ("file<with<less<than.mp4"),
        ("file>with>greater>than.mp4"),
        ("file:with:colons.mp4"),
        ('file"with"quotes.mp4'),
        ("file|with|pipes.mp4"),
        (""),
        (None),
    ],
)
def test_valid_filename_invalid_filenames(filename: str):
    with pytest.raises(ValidationException):
        valid_filename(filename, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_filename(filename, from_cli=True)


def test_valid_image_format_with_valid_lowercase_image_formats():
    for image_format in C.VALID_IMAGE_FORMATS:
        assert valid_image_format(image_format) == image_format


def test_valid_image_format_with_valid_uppercase_image_formats():
    for image_format in C.VALID_IMAGE_FORMATS:
        assert valid_image_format(image_format.upper()) == image_format


def test_valid_image_format_with_valid_lowercase_image_formats_with_dot():
    for image_format in C.VALID_IMAGE_FORMATS:
        assert valid_image_format(f".{image_format}") == image_format


def test_valid_image_format_with_valid_uppercase_image_formats_with_dot():
    for image_format in C.VALID_IMAGE_FORMATS:
        assert valid_image_format(f".{image_format.upper()}") == image_format


@pytest.mark.parametrize(
    ("timestamp", "expected"),
    [
        ("0:00", "0:00"),
        ("00:00", "00:00"),
        ("0:00:00", "0:00:00"),
        ("00:00:00", "00:00:00"),
        ("0:00:00.0", "0:00:00"),
        ("0:00:00.01", "0:00:00"),
        ("0:00:00.99", "0:00:00"),
        ("12:34:56", "12:34:56"),
        ("1:23:45", "1:23:45"),
        ("12:34", "12:34"),
        ("1:23", "1:23"),
        ("59:59:59", "59:59:59"),
    ],
)
def test_valid_timestamp_valid(timestamp: str, expected: str):
    assert valid_timestamp(timestamp, from_cli=False) == expected
    assert valid_timestamp(timestamp, from_cli=True) == expected


@pytest.mark.parametrize(
    ("timestamp"),
    [
        (""),
        (" "),
        (":"),
        ("0"),
        ("00"),
        (":0"),
        (":00"),
        ("0:"),
        ("00:"),
        ("0:0"),
        ("00:0"),
        ("0:0:0"),
        ("0:0:00"),
        ("0:00:0"),
        ("00:0:0"),
        ("00:00:0"),
        ("60:00:00"),
        ("00:60:00"),
        ("00:00:60"),
        ("60:60:60"),
        ("abc"),
        ("ab:cd:ef"),
        ("x0:00:00"),
        ("0x:00:00"),
        ("00:x0:00"),
        ("00:0x:00"),
        ("00:00:x0"),
        ("00:00:0x"),
        (None),
    ],
)
def test_valid_timestamp_invalid(timestamp: str):
    with pytest.raises(ValidationException):
        valid_timestamp(timestamp, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_timestamp(timestamp, from_cli=True)


@pytest.mark.parametrize(
    ("capture_rate", "first_frame", "last_frame", "expected"),
    [
        (1, 0, 2, 1),  # capture rate (1) < number of frames to capture (2)
        (29, 0, 30, 29),  # capture rate (29) < number of frames to capture (30)
        (50, 30, 90, 50),  # capture rate (50) < number of frames to capture (60)
        (1, 0, 1, 1),  # capture rate (1) == number of frames to capture (1)
        (50, 30, 80, 50),  # capture rate (50) == number of frames to capture (50)
    ],
)
def test_valid_capture_rate_with_valid_capture_rates(
    capture_rate: int, first_frame: int, last_frame: int, expected: int
):
    assert valid_capture_rate(capture_rate, first_frame, last_frame) == expected


@pytest.mark.parametrize(
    ("capture_rate", "first_frame", "last_frame"),
    [
        (-1, 0, 1),  # capture rate cannot be negative
        (0, 0, 1),  # capture rate cannot be (0)
        (2, 0, 1),  # capture rate (2) > number of frames to capture (1)
    ],
)
def test_valid_capture_rate_invalid_capture_rates_raises_validation_exception(
    capture_rate: int, first_frame: int, last_frame: int
):
    with pytest.raises(ValidationException):
        valid_capture_rate(capture_rate, first_frame, last_frame)


def test_valid_resize_value_with_valid_resize_values_strings():
    assert valid_resize_value("0.01") == 0.01
    assert valid_resize_value("0.1") == 0.1
    assert valid_resize_value("1") == 1
    assert valid_resize_value("1.0") == 1.0
    assert valid_resize_value("50.0") == 50.0


def test_valid_resize_value_with_valid_resize_values_floats():
    assert valid_resize_value(0.01) == 0.01
    assert valid_resize_value(0.1) == 0.1
    assert valid_resize_value(1) == 1
    assert valid_resize_value(1.0) == 1.0
    assert valid_resize_value(50.0) == 50.0


def test_valid_resize_value_with_valid_ints():
    assert valid_resize_value(1) == 1
    assert valid_resize_value(50) == 50


def test_valid_dimensions_with_valid_dimensions():
    assert valid_dimensions((1, 1)) == (1, 1)
    assert valid_dimensions((1, 100_000_000)) == (1, 100_000_000)
    assert valid_dimensions((100_000_000, 1)) == (100_000_000, 1)
    assert valid_dimensions((100_000_000, 100_000_000)) == (100_000_000, 100_000_000)


def test_valid_rotate_value_with_valid_rotate_ints():
    for rotate_value in C.VALID_ROTATE_VALUES:
        assert valid_rotate_value(rotate_value) == rotate_value


def test_valid_rotate_value_with_valid_rotate_floats():
    for rotate_value in C.VALID_ROTATE_VALUES:
        assert valid_rotate_value(float(rotate_value)) == rotate_value


def test_valid_rotate_value_with_valid_rotate_int_strings():
    for rotate_value in C.VALID_ROTATE_VALUES:
        assert valid_rotate_value(str(rotate_value)) == rotate_value


def test_valid_start_time_with_valid_start_time_strings():
    assert valid_start_time("0") == 0.0
    assert valid_start_time("60") == 60.0
    assert valid_start_time("0:00") == "0:00"
    assert valid_start_time("0:00:00") == "0:00:00"
    assert valid_start_time("0:00:00.0") == "0:00:00"
    assert valid_start_time("0:00:00.9") == "0:00:00"


def test_valid_start_time_with_valid_start_time_ints():
    assert valid_start_time(0) == 0
    assert valid_start_time(1) == 1
    assert valid_start_time(60) == 60
    assert valid_start_time(3600) == 3600


def test_valid_start_time_with_valid_start_time_floats():
    assert valid_start_time(0.0) == 0.0
    assert valid_start_time(0.9) == 0.9
    assert valid_start_time(1.0) == 1.0
    assert valid_start_time(1.9) == 1.9
    assert valid_start_time(60.0) == 60.0
    assert valid_start_time(60.9) == 60.9
    assert valid_start_time(3600.0) == 3600.0
    assert valid_start_time(3600.9) == 3600.9


def test_valid_stop_time_with_valid_stop_time_strings():
    assert valid_stop_time("1") == 1.0
    assert valid_stop_time("60") == 60.0
    assert valid_stop_time("1:00") == "1:00"
    assert valid_stop_time("1:00:00") == "1:00:00"
    assert valid_stop_time("1:00:00.0") == "1:00:00"
    assert valid_stop_time("1:00:00.9") == "1:00:00"


def test_valid_stop_time_with_valid_stop_time_ints():
    assert valid_stop_time(1) == 1
    assert valid_stop_time(60) == 60
    assert valid_stop_time(3600) == 3600


def test_valid_stop_time_with_valid_stop_time_floats():
    assert valid_stop_time(0.01) == 0.01
    assert valid_stop_time(1.0) == 1.0
    assert valid_stop_time(1.9) == 1.9
    assert valid_stop_time(60.0) == 60.0
    assert valid_stop_time(60.9) == 60.9
    assert valid_stop_time(3600.0) == 3600.0
    assert valid_stop_time(3600.9) == 3600.9


def test_valid_video_filepath_with_supported_existing_filepath(
    tmp_video_filepath: Path,
):
    """Test that a filepath is returned when an existing, supported pathlib video filepath is passed.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    assert (
        valid_video_filepath(tmp_video_filepath, from_cli=False) == tmp_video_filepath
    )
    assert valid_video_filepath(tmp_video_filepath, from_cli=True) == tmp_video_filepath


def test_valid_video_filepath_with_supported_existing_filepath_string(
    tmp_video_filepath: Path,
):
    """Test that a filepath is returned when an existing, supported pathlib video filepath string is passed.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    path_str = str(tmp_video_filepath)
    assert valid_video_filepath(path_str, from_cli=False) == tmp_video_filepath
    assert valid_video_filepath(path_str, from_cli=True) == tmp_video_filepath


def test_valid_video_filepath_with_supported_existing_filepath_lowercase_suffix(
    tmp_video_filepath: Path,
):
    """Test that a filepath is returned when an existing, supported pathlib video filepath is passed with a lowercase suffix.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    path = tmp_video_filepath.with_suffix(".mp4")
    assert valid_video_filepath(path, from_cli=False) == tmp_video_filepath
    assert valid_video_filepath(path, from_cli=True) == tmp_video_filepath


def test_valid_video_filepath_with_supported_existing_filepath_mixedcase_suffix(
    tmp_video_filepath: Path,
):
    """Test that a filepath is returned when an existing, supported pathlib video filepath is passed with a mixedcase suffix.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    path = tmp_video_filepath.with_suffix(".Mp4")
    assert valid_video_filepath(path, from_cli=False) == tmp_video_filepath
    assert valid_video_filepath(path, from_cli=True) == tmp_video_filepath


def test_valid_video_filepath_with_supported_existing_filepath_uppercase_suffix(
    tmp_video_filepath: Path,
):
    """Test that a filepath is returned when an existing, supported pathlib video filepath is passed with an uppercase suffix.

    `tmp_video_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    path = tmp_video_filepath.with_suffix(".MP4")
    assert valid_video_filepath(path, from_cli=False) == tmp_video_filepath
    assert valid_video_filepath(path, from_cli=True) == tmp_video_filepath


def test_valid_video_filepath_with_supported_nonexistant_video_filepath(tmp_path: Path):
    """Test that a ValidationException is raised when a nonexistant, supported pathlib video filepath is passed.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    path = tmp_path / "t.mp4"
    with pytest.raises(ValidationException):
        valid_video_filepath(path, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_video_filepath(path, from_cli=True)


def test_valid_video_filepath_with_supported_nonexistant_video_filepath_string():
    """Test that a ValidationException is raised when a nonexistant, supported pathlib video filepath string is passed.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    with pytest.raises(ValidationException):
        valid_video_filepath("t.mp4", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_video_filepath("t.mp4", from_cli=True)


def test_valid_video_filepath_with_unsupported_existing_file_suffix(
    tmp_text_filepath: Path,
):
    """Test that a ValidationException is raised when an existing, unsupported pathlib filepath is passed.

    `tmp_text_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    with pytest.raises(ValidationException):
        valid_video_filepath(tmp_text_filepath, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_video_filepath(tmp_text_filepath, from_cli=True)


def test_valid_video_filepath_with_unsupported_nonexistant_file_suffix():
    """Test that a ValidationException is raised when a nonexistant, unsupported string filepath is passed.

    `tmp_text_filepath` is created by the fixture of the same name in `conftest.py`.
    """
    with pytest.raises(ValidationException):
        valid_video_filepath("t.txt", from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_video_filepath("t.txt", from_cli=True)


def test_valid_video_filepath_with_directory_path(tmp_path: Path):
    """Test that a ValidationException is raised when a pathlib directory path is passed.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    with pytest.raises(ValidationException):
        valid_video_filepath(tmp_path, from_cli=False)
    with pytest.raises(ArgumentTypeError):
        valid_video_filepath(tmp_path, from_cli=True)


def test__raise_error_from_cli_raising_arguement_type_error():
    error_msg = "Argument type error"
    with pytest.raises(ArgumentTypeError) as excinfo:
        _raise_error(error_msg, from_cli=True)
    assert error_msg in str(excinfo.value)


def test__raise_error_from_non_cli_raising_validation_error():
    error_msg = "Validation exception"
    with pytest.raises(ValidationException) as excinfo:
        _raise_error(error_msg, from_cli=False)
    assert error_msg in str(excinfo.value)


class TestNonCLI:
    # valid_image_format
    def test_valid_image_format_with_invalid_format_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_image_format("invalid")

    # valid_resize_value
    def test_valid_resize_value_with_invalid_value_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_resize_value("invalid")

    def test_valid_resize_value_with_invalid_ints_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_resize_value(-1)
        with pytest.raises(ValidationException):
            valid_resize_value(0)

    def test_valid_resize_value_with_invalid_floats_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_resize_value(-1.0)
        with pytest.raises(ValidationException):
            valid_resize_value(0.0)
        with pytest.raises(ValidationException):
            valid_resize_value(0.009)

    def test_valid_resize_value_with_invalid_strings_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_resize_value("-1")
        with pytest.raises(ValidationException):
            valid_resize_value("0")
        with pytest.raises(ValidationException):
            valid_resize_value("-1.0")
        with pytest.raises(ValidationException):
            valid_resize_value("0.0")
        with pytest.raises(ValidationException):
            valid_resize_value("0.009")

    # valid_dimensions
    def test_valid_dimensions_with_invalid_ints_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_dimensions((-1, -1))
        with pytest.raises(ValidationException):
            valid_dimensions((0, 0))

    def test_valid_dimensions_with_invalid_floats_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_dimensions((-1.0, -1.0))
        with pytest.raises(ValidationException):
            valid_dimensions((0.0, 0.0))
        with pytest.raises(ValidationException):
            valid_dimensions((0.009, 0.009))

    def test_valid_dimensions_with_invalid_strings_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_dimensions(("-1", "-1"))
        with pytest.raises(ValidationException):
            valid_dimensions(("0", "0"))
        with pytest.raises(ValidationException):
            valid_dimensions(("-1.0", "-1.0"))
        with pytest.raises(ValidationException):
            valid_dimensions(("0.0", "0.0"))
        with pytest.raises(ValidationException):
            valid_dimensions(("0.009", "0.009"))

    def test_valid_dimensions_with_more_than_two_values_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_dimensions((1, 2, 3))

    def test_test_valid_dimensions_with_less_than_two_values_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_dimensions((1,))

    # valid_rotate_value
    def test_valid_rotate_value_with_invalid_value_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_rotate_value("invalid")

    def test_valid_rotate_value_with_invalid_float_string_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_rotate_value("0.1")

    # valid_start_time
    def test_valid_start_time_with_invalid_value_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_start_time("invalid")

    def test_valid_start_time_with_invalid_float_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_start_time(-1.0)

    def test_valid_start_time_with_invalid_float_string_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_start_time("-1.0")

    def test_valid_start_time_with_invalid_int_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_start_time(-1)

    def test_valid_start_time_with_invalid_int_string_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_start_time("-1")

    # valid_stop_time
    def test_valid_stop_time_with_invalid_value_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_stop_time("invalid")

    def test_valid_stop_time_with_invalid_float_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_stop_time(-1.0)
        with pytest.raises(ValidationException):
            valid_stop_time(0.0)

    def test_valid_stop_time_with_invalid_float_string_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_stop_time("-1.0")
        with pytest.raises(ValidationException):
            valid_stop_time("0.0")

    def test_valid_stop_time_with_invalid_int_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_stop_time(-1)
        with pytest.raises(ValidationException):
            valid_stop_time(0)

    def test_valid_stop_time_with_invalid_int_string_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_stop_time("-1")
        with pytest.raises(ValidationException):
            valid_stop_time("0")
