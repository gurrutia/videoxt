import argparse
import os

import pytest

import videoxt.constants as C
from videoxt.validators import non_negative_float
from videoxt.validators import non_negative_int
from videoxt.validators import positive_float
from videoxt.validators import positive_int
from videoxt.validators import valid_dir
from videoxt.validators import valid_filename
from videoxt.validators import valid_filepath
from videoxt.validators import valid_image_format
from videoxt.validators import valid_resize_value
from videoxt.validators import valid_timestamp
from videoxt.validators import ValidationException


def test_positive_int_with_positive_ints():
    assert positive_int(1) == 1
    assert positive_int("1") == 1
    assert positive_int(100_000_000) == 100_000_000
    assert positive_int("100_000_000") == 100_000_000


def test_positive_int_with_valid_floats():
    assert positive_int(1.0) == 1
    assert positive_int("1.0") == 1
    assert positive_int(100_000_000.0) == 100_000_000
    assert positive_int("100_000_000.0") == 100_000_000


def test_positive_float_with_positive_floats():
    assert positive_float(1.0) == 1.0
    assert positive_float("1.0") == 1.0
    assert positive_float(12.34) == 12.34
    assert positive_float("12.34") == 12.34
    assert positive_float(100_000_000.0) == 100_000_000.0
    assert positive_float("100_000_000.0") == 100_000_000.0


def test_positive_float_with_positive_ints():
    assert positive_float(1) == 1.0
    assert positive_float("1") == 1.0
    assert positive_float(100_000_000) == 100_000_000.0
    assert positive_float("100_000_000") == 100_000_000.0


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


def test_valid_filepath_with_valid_string_filepath(tmp_path):
    filepath = tmp_path / "t.txt"
    filepath.write_text("t")
    assert valid_filepath(str(filepath)) == str(filepath)
    os.remove(filepath)


def test_valid_filepath_with_valid_pathlib_filepath(tmp_path):
    filepath = tmp_path / "t.txt"
    filepath.write_text("t")
    assert valid_filepath(filepath) == str(filepath)
    os.remove(filepath)


def test_valid_dir_with_valid_string_dir(tmp_path):
    dirpath = tmp_path / "t"
    dirpath.mkdir()
    assert valid_dir(str(dirpath)) == str(dirpath)
    os.rmdir(dirpath)


def test_valid_dir_with_valid_pathlib_dir(tmp_path):
    dirpath = tmp_path / "t"
    dirpath.mkdir()
    assert valid_dir(dirpath) == str(dirpath)
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
    assert valid_timestamp(timestamp="0", timestamp_type="start") == "0"
    assert valid_timestamp(timestamp="0:00", timestamp_type="start") == "0:00"
    assert valid_timestamp(timestamp="0:00:00", timestamp_type="start") == "0:00:00"
    assert valid_timestamp(timestamp="0:00:00.0", timestamp_type="start") == "0:00:00"
    assert valid_timestamp(timestamp="0:00:00.9", timestamp_type="start") == "0:00:00"


def test_valid_timestamp_with_valid_start_timestamp_non_zero():
    for timestamp_type in ("start", "stop"):
        assert valid_timestamp("1", timestamp_type) == "1"
        assert valid_timestamp("1:00", timestamp_type) == "1:00"
        assert valid_timestamp("1:00:00", timestamp_type) == "1:00:00"
        assert valid_timestamp("1:00:00.0", timestamp_type) == "1:00:00"
        assert valid_timestamp("1:00:00.1", timestamp_type) == "1:00:00"
        assert valid_timestamp("61", timestamp_type) == "61"
        assert valid_timestamp("59:59", timestamp_type) == "59:59"
        assert valid_timestamp("59:59:59", timestamp_type) == "59:59:59"
        assert valid_timestamp("59:59:59.0", timestamp_type) == "59:59:59"
        assert valid_timestamp("59:59:59.9", timestamp_type) == "59:59:59"


def test_valid_timestamp_without_timestamp_type():
    with pytest.raises(TypeError):
        valid_timestamp("0")


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


class TestNonTerminal:
    C.IS_TERMINAL = False

    # positive_int
    def test_positive_int_with_zero_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_int(0)

    def test_positive_int_with_zero_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_int("0")

    def test_positive_int_with_negative_int_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_int(-1)

    def test_positive_int_with_negative_int_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_int("-1")

    def test_positive_int_with_invalid_float_from_non_terminal_0_9(self):
        with pytest.raises(ValidationException):
            positive_int(0.9)

    def test_positive_int_with_invalid_float_string_from_non_terminal_0_9_string(self):
        with pytest.raises(ValidationException):
            positive_int("0.9")

    def test_positive_int_with_invalid_float_from_non_terminal_1_1(self):
        with pytest.raises(ValidationException):
            positive_int(1.1)

    def test_positive_int_with_invalid_float_string_from_non_terminal_1_1_string(self):
        with pytest.raises(ValidationException):
            positive_int("1.1")

    def test_positive_int_with_non_int_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_int("a")

    # positive_float
    def test_positive_float_with_zero_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_float(0)

    def test_positive_float_with_zero_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_float("0")

    def test_positive_float_with_negative_float_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_float(-1.0)

    def test_positive_float_with_negative_float_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_float("-1.0")

    def test_positive_float_with_non_float_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_float("a")

    # non_negative_int
    def test_non_negative_int_with_negative_int_from_non_terminal(self):
        with pytest.raises(ValidationException):
            non_negative_int(-1)

    def test_non_negative_int_with_negative_int_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            non_negative_int("-1")

    def test_non_negative_int_with_invalid_float_from_non_terminal_1_1(self):
        with pytest.raises(ValidationException):
            non_negative_int(1.1)

    def test_non_negative_int_with_invalid_float_from_non_terminal_0_9(self):
        with pytest.raises(ValidationException):
            non_negative_int(0.9)

    def test_non_negative_int_with_invalid_float_from_non_terminal_1_1_string(self):
        with pytest.raises(ValidationException):
            non_negative_int("1.1")

    def test_non_negative_int_with_invalid_float_from_non_terminal_0_9_string(self):
        with pytest.raises(ValidationException):
            non_negative_int("0.9")

    def test_non_negative_int_with_non_int_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            non_negative_int("a")

    # non_negative_float
    def test_non_negative_float_with_negative_float_from_non_terminal(self):
        with pytest.raises(ValidationException):
            non_negative_float(-1.0)

    def test_non_negative_float_with_negative_float_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            non_negative_float("-1.0")

    def test_non_negative_float_with_non_float_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            non_negative_float("a")

    # valid_filepath
    def test_valid_filepath_with_invalid_filepath_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_filepath("invalid.txt")

    def test_invalid_filepath_with_non_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_filepath(1)

    # valid_dir
    def test_valid_dir_with_invalid_dir_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_dir("invalid")

    def test_valid_dir_with_non_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_dir(1)

    # valid_filename
    def test_valid_filename_with_slashes(self):
        with pytest.raises(ValidationException):
            valid_filename("file/with/slashes.txt")

    def test_valid_filename_with_backslashes(self):
        with pytest.raises(ValidationException):
            valid_filename("file\\with\\backslashes.txt")

    def test_valid_filename_with_colons(self):
        with pytest.raises(ValidationException):
            valid_filename("file:with:colons.txt")

    def test_valid_filename_with_question_marks(self):
        with pytest.raises(ValidationException):
            valid_filename("file?with?question?marks.txt")

    def test_valid_filename_with_asterisks(self):
        with pytest.raises(ValidationException):
            valid_filename("file*with*asterisks.txt")

    def test_valid_filename_with_quotes(self):
        with pytest.raises(ValidationException):
            valid_filename('file"with"quotes.txt')

    def test_valid_filename_with_less_than(self):
        with pytest.raises(ValidationException):
            valid_filename("file<with<less<than.txt")

    def test_valid_filename_with_greater_than(self):
        with pytest.raises(ValidationException):
            valid_filename("file>with>greater>than.txt")

    def test_valid_filename_with_pipes(self):
        with pytest.raises(ValidationException):
            valid_filename("file|with|pipes.txt")

    # valid_image_format
    def test_valid_image_format_with_invalid_format_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_image_format("invalid")

    # valid_timestamp
    def test_valid_timestamp_containing_colon_from_non_terminal(self):
        for timestamp_type in ("start", "stop"):
            with pytest.raises(ValidationException):
                valid_timestamp("x0:00:00", timestamp_type)
            with pytest.raises(ValidationException):
                valid_timestamp("0x:00:00", timestamp_type)
            with pytest.raises(ValidationException):
                valid_timestamp("00:x0:00", timestamp_type)
            with pytest.raises(ValidationException):
                valid_timestamp("00:0x:00", timestamp_type)
            with pytest.raises(ValidationException):
                valid_timestamp("00:00:x0", timestamp_type)
            with pytest.raises(ValidationException):
                valid_timestamp("00:00:0x", timestamp_type)

    def test_valid_timestamp_with_invalid_timestamp_60_from_non_terminal(self):
        for timestamp_type in ("start", "stop"):
            with pytest.raises(ValidationException):
                valid_timestamp("60:00:00", timestamp_type)
            with pytest.raises(ValidationException):
                valid_timestamp("60:00", timestamp_type)
            with pytest.raises(ValidationException):
                valid_timestamp("1:60", timestamp_type)

    def test_valid_timestamp_with_invalid_start_timestamp_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_timestamp("-1", "start")

    def test_valid_timestamp_with_invalid_stop_timestamp_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_timestamp("-1", "stop")
        with pytest.raises(ValidationException):
            valid_timestamp("0", "stop")
        with pytest.raises(ValidationException):
            valid_timestamp("0.9", "stop")

    # valid_resize_value
    def test_valid_resize_value_with_invalid_value_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_resize_value("invalid")

    def test_valid_resize_value_with_invalid_ints(self):
        with pytest.raises(ValidationException):
            valid_resize_value(-1)
        with pytest.raises(ValidationException):
            valid_resize_value(0)

    def test_valid_resize_value_with_invalid_floats(self):
        with pytest.raises(ValidationException):
            valid_resize_value(-1.0)
        with pytest.raises(ValidationException):
            valid_resize_value(0.0)
        with pytest.raises(ValidationException):
            valid_resize_value(0.009)

    def test_valid_resize_value_with_invalid_strings(self):
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
