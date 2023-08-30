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


def test_non_negative_int_with_non_negative_ints():
    assert non_negative_int(0) == 0
    assert non_negative_int("0") == 0
    assert non_negative_int(1) == 1
    assert non_negative_int("1") == 1
    assert non_negative_int(100_000_000) == 100_000_000
    assert non_negative_int("100_000_000") == 100_000_000


def test_non_negative_int_with_non_negative_floats():
    assert non_negative_int(0.0) == 0
    assert non_negative_int("0.0") == 0
    assert non_negative_int(1.0) == 1
    assert non_negative_int("1.0") == 1
    assert non_negative_int(100_000_000.0) == 100_000_000
    assert non_negative_int("100_000_000.0") == 100_000_000


def test_non_negative_float_with_non_negative_floats():
    assert non_negative_float(0.0) == 0.0
    assert non_negative_float("0.0") == 0.0
    assert non_negative_float(1.0) == 1.0
    assert non_negative_float("1.0") == 1.0
    assert non_negative_float(12.34) == 12.34
    assert non_negative_float("12.34") == 12.34
    assert non_negative_float(100_000_000.0) == 100_000_000.0
    assert non_negative_float("100_000_000.0") == 100_000_000.0


def test_non_negative_float_with_non_negative_ints():
    assert non_negative_float(0) == 0.0
    assert non_negative_float("0") == 0.0
    assert non_negative_float(1) == 1.0
    assert non_negative_float("1") == 1.0
    assert non_negative_float(100_000_000) == 100_000_000.0
    assert non_negative_float("100_000_000") == 100_000_000.0


def test_valid_filepath_with_valid_string_filepath(tmp_path: Path):
    """Test that a valid filepath is returned when a valid string filepath is passed.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    filepath = tmp_path / "t.txt"
    filepath.write_text("t")
    assert valid_filepath(str(filepath)) == filepath
    os.remove(filepath)


def test_valid_filepath_with_valid_pathlib_filepath(tmp_path: Path):
    """Test that a valid filepath is returned when a valid pathlib filepath is passed.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    filepath = tmp_path / "t.txt"
    filepath.write_text("t")
    assert valid_filepath(filepath) == filepath
    os.remove(filepath)


def test_valid_dir_with_valid_dir_string(tmp_path: Path):
    """Test that a valid directory is returned when a valid string directory is passed.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    dirpath = tmp_path / "t"
    dirpath.mkdir()
    assert valid_dir(str(dirpath)) == dirpath
    os.rmdir(dirpath)


def test_valid_dir_with_valid_dir_pathlib(tmp_path: Path):
    """Test that a valid directory is returned when a valid pathlib directory is passed.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    dirpath = tmp_path / "t"
    dirpath.mkdir()
    assert valid_dir(dirpath) == dirpath
    os.rmdir(dirpath)


def test_valid_filename_with_valid_filename():
    assert valid_filename("file.txt") == "file.txt"
    assert valid_filename("file_with_underscores.txt") == "file_with_underscores.txt"
    assert valid_filename("file-with-dashes.txt") == "file-with-dashes.txt"
    assert valid_filename("file (1).txt") == "file (1).txt"


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


def test_valid_timestamp_with_valid_start_timestamp_zero():
    assert valid_timestamp(timestamp="0:00") == "0:00"
    assert valid_timestamp(timestamp="0:00:00") == "0:00:00"
    assert valid_timestamp(timestamp="0:00:00.0") == "0:00:00"
    assert valid_timestamp(timestamp="0:00:00.9") == "0:00:00"


def test_valid_timestamp_with_valid_start_timestamp_non_zero():
    assert valid_timestamp("1:00") == "1:00"
    assert valid_timestamp("1:00:00") == "1:00:00"
    assert valid_timestamp("1:00:00.0") == "1:00:00"
    assert valid_timestamp("1:00:00.1") == "1:00:00"
    assert valid_timestamp("59:59") == "59:59"
    assert valid_timestamp("59:59:59") == "59:59:59"
    assert valid_timestamp("59:59:59.0") == "59:59:59"
    assert valid_timestamp("59:59:59.9") == "59:59:59"


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


def test_valid_capture_rate_with_valid_capture_rates():
    assert valid_capture_rate(1, 0, 1) == 1
    assert valid_capture_rate(12, 0, 12) == 12
    assert valid_capture_rate(24, 0, 24) == 24
    assert valid_capture_rate(30, 0, 30) == 30
    assert valid_capture_rate(60, 0, 60) == 60
    assert valid_capture_rate(120, 0, 120) == 120
    assert valid_capture_rate(240, 0, 240) == 240


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
    # non_negative_int
    def test_non_negative_int_with_negative_int_from_non_cli(self):
        with pytest.raises(ValidationException):
            non_negative_int(-1)

    def test_non_negative_int_with_negative_int_string_from_non_cli(self):
        with pytest.raises(ValidationException):
            non_negative_int("-1")

    def test_non_negative_int_with_invalid_float_from_non_cli_1_1(self):
        with pytest.raises(ValidationException):
            non_negative_int(1.1)

    def test_non_negative_int_with_invalid_float_from_non_cli_0_9(self):
        with pytest.raises(ValidationException):
            non_negative_int(0.9)

    def test_non_negative_int_with_invalid_float_from_non_cli_1_1_string(self):
        with pytest.raises(ValidationException):
            non_negative_int("1.1")

    def test_non_negative_int_with_invalid_float_from_non_cli_0_9_string(self):
        with pytest.raises(ValidationException):
            non_negative_int("0.9")

    def test_non_negative_int_with_non_int_string_from_non_cli(self):
        with pytest.raises(ValidationException):
            non_negative_int("a")

    # non_negative_float
    def test_non_negative_float_with_negative_float_from_non_cli(self):
        with pytest.raises(ValidationException):
            non_negative_float(-1.0)

    def test_non_negative_float_with_negative_float_string_from_non_cli(self):
        with pytest.raises(ValidationException):
            non_negative_float("-1.0")

    def test_non_negative_float_with_non_float_string_from_non_cli(self):
        with pytest.raises(ValidationException):
            non_negative_float("a")

    # valid_filepath
    def test_valid_filepath_with_invalid_string_filepath_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filepath("invalid.txt")

    def test_valid_filepath_with_invalid_pathlib_filepath_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filepath(Path("invalid.txt"))

    # valid_dir
    def test_valid_dir_with_invalid_dir_string_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_dir("invalid")

    def test_valid_dir_with_invalid_dir_pathlib_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_dir(Path("invalid"))

    # valid_filename
    def test_valid_filename_with_slashes_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filename("file/with/slashes.txt")

    def test_valid_filename_with_backslashes_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filename("file\\with\\backslashes.txt")

    def test_valid_filename_with_colons_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filename("file:with:colons.txt")

    def test_valid_filename_with_question_marks_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filename("file?with?question?marks.txt")

    def test_valid_filename_with_asterisks_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filename("file*with*asterisks.txt")

    def test_valid_filename_with_quotes_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filename('file"with"quotes.txt')

    def test_valid_filename_with_less_than_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filename("file<with<less<than.txt")

    def test_valid_filename_with_greater_than_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filename("file>with>greater>than.txt")

    def test_valid_filename_with_pipes_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_filename("file|with|pipes.txt")

    # valid_image_format
    def test_valid_image_format_with_invalid_format_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_image_format("invalid")

    # valid_timestamp
    def test_valid_timestamp_containing_colon_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_timestamp("x0:00:00")
        with pytest.raises(ValidationException):
            valid_timestamp("0x:00:00")
        with pytest.raises(ValidationException):
            valid_timestamp("00:x0:00")
        with pytest.raises(ValidationException):
            valid_timestamp("00:0x:00")
        with pytest.raises(ValidationException):
            valid_timestamp("00:00:x0")
        with pytest.raises(ValidationException):
            valid_timestamp("00:00:0x")

    def test_valid_timestamp_with_invalid_timestamp_60_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_timestamp("60:00:00")
        with pytest.raises(ValidationException):
            valid_timestamp("60:00")
        with pytest.raises(ValidationException):
            valid_timestamp("1:60")

    def test_valid_timestamp_with_invalid_start_timestamp_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_timestamp("-1:")

    def test_valid_timestamp_with_invalid_stop_timestamp_from_non_cli(self):
        with pytest.raises(ValidationException):
            valid_timestamp("-1:")
        with pytest.raises(ValidationException):
            valid_timestamp("0::")
        with pytest.raises(ValidationException):
            valid_timestamp(":0.9")

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

    # valid_extraction_range
    def test_valid_extraction_range_where_start_second_greater_than_video_length_second_from_non_cli(
        self,
    ):
        with pytest.raises(ValidationException):
            valid_extraction_range(2.0, 1.0, 1.0)

    def test_valid_extraction_range_where_start_second_greater_than_stop_second(
        self,
    ):
        with pytest.raises(ValidationException):
            valid_extraction_range(2.0, 1.0, 3.0)

    # valid_capture_rate
    def test_valid_capture_rate_where_capture_rate_greater_than_frame_range_from_non_cli(
        self,
    ):
        with pytest.raises(ValidationException):
            valid_capture_rate(1, 1, 1)

    def test_valid_capture_rate_where_capture_rate_greater_than_frame_range_from_non_cli(
        self,
    ):
        with pytest.raises(ValidationException):
            valid_capture_rate(100_000_000, 0, 30)
