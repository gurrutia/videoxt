import argparse
import os

import pytest

import videoxt.constants as C
from videoxt.validators import non_negative_float
from videoxt.validators import non_negative_int
from videoxt.validators import positive_float
from videoxt.validators import positive_int
from videoxt.validators import valid_capture_rate
from videoxt.validators import valid_dimensions
from videoxt.validators import valid_dir
from videoxt.validators import valid_filename
from videoxt.validators import valid_filepath
from videoxt.validators import valid_image_format
from videoxt.validators import valid_resize_value
from videoxt.validators import valid_rotate_value
from videoxt.validators import valid_start_time
from videoxt.validators import valid_stop_time
from videoxt.validators import valid_timestamp
from videoxt.validators import validate_video_extraction_range
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


def test_valid_rotate_value_with_valid_rotate_float_strings():
    for rotate_value in C.VALID_ROTATE_VALUES:
        assert valid_rotate_value(str(float(rotate_value))) == rotate_value


def test_valid_start_time_with_valid_start_time_strings():
    assert valid_start_time("0") == "0"
    assert valid_start_time("0:00") == "0:00"
    assert valid_start_time("0:00:00") == "0:00:00"
    assert valid_start_time("0:00:00.0") == "0:00:00"
    assert valid_start_time("0:00:00.9") == "0:00:00"
    assert valid_start_time("60") == "60"


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
    assert valid_stop_time("1") == "1"
    assert valid_stop_time("1:00") == "1:00"
    assert valid_stop_time("1:00:00") == "1:00:00"
    assert valid_stop_time("1:00:00.0") == "1:00:00"
    assert valid_stop_time("1:00:00.9") == "1:00:00"
    assert valid_stop_time("60") == "60"


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
    def test_valid_filename_with_slashes_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_filename("file/with/slashes.txt")

    def test_valid_filename_with_backslashes_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_filename("file\\with\\backslashes.txt")

    def test_valid_filename_with_colons_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_filename("file:with:colons.txt")

    def test_valid_filename_with_question_marks_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_filename("file?with?question?marks.txt")

    def test_valid_filename_with_asterisks_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_filename("file*with*asterisks.txt")

    def test_valid_filename_with_quotes_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_filename('file"with"quotes.txt')

    def test_valid_filename_with_less_than_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_filename("file<with<less<than.txt")

    def test_valid_filename_with_greater_than_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_filename("file>with>greater>than.txt")

    def test_valid_filename_with_pipes_from_non_terminal(self):
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

    def test_valid_resize_value_with_invalid_ints_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_resize_value(-1)
        with pytest.raises(ValidationException):
            valid_resize_value(0)

    def test_valid_resize_value_with_invalid_floats_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_resize_value(-1.0)
        with pytest.raises(ValidationException):
            valid_resize_value(0.0)
        with pytest.raises(ValidationException):
            valid_resize_value(0.009)

    def test_valid_resize_value_with_invalid_strings_from_non_terminal(self):
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
    def test_valid_dimensions_with_invalid_ints_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_dimensions((-1, -1))
        with pytest.raises(ValidationException):
            valid_dimensions((0, 0))

    def test_valid_dimensions_with_invalid_floats_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_dimensions((-1.0, -1.0))
        with pytest.raises(ValidationException):
            valid_dimensions((0.0, 0.0))
        with pytest.raises(ValidationException):
            valid_dimensions((0.009, 0.009))

    def test_valid_dimensions_with_invalid_strings_from_non_terminal(self):
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

    def test_valid_dimensions_with_more_than_two_values_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_dimensions((1, 2, 3))

    def test_test_valid_dimensions_with_less_than_two_values_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_dimensions((1,))

    # valid_rotate_value
    def test_valid_rotate_value_with_invalid_value_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_rotate_value("invalid")

    def test_valid_rotate_value_with_invalid_float_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_rotate_value(0.1)

    def test_valid_rotate_value_with_invalid_float_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_rotate_value("0.1")

    # valid_start_time
    def test_valid_start_time_with_invalid_value_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_start_time("invalid")

    def test_valid_start_time_with_invalid_float_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_start_time(-1.0)

    def test_valid_start_time_with_invalid_float_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_start_time("-1.0")

    def test_valid_start_time_with_invalid_int_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_start_time(-1)

    def test_valid_start_time_with_invalid_int_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_start_time("-1")

    # valid_stop_time
    def test_valid_stop_time_with_invalid_value_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_stop_time("invalid")

    def test_valid_stop_time_with_invalid_float_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_stop_time(-1.0)
        with pytest.raises(ValidationException):
            valid_stop_time(0.0)

    def test_valid_stop_time_with_invalid_float_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_stop_time("-1.0")
        with pytest.raises(ValidationException):
            valid_stop_time("0.0")

    def test_valid_stop_time_with_invalid_int_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_stop_time(-1)
        with pytest.raises(ValidationException):
            valid_stop_time(0)

    def test_valid_stop_time_with_invalid_int_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            valid_stop_time("-1")
        with pytest.raises(ValidationException):
            valid_stop_time("0")

    # validate_video_extraction_range
    def test_validate_video_extraction_range_where_start_second_greater_than_video_length_second_from_non_terminal(
        self,
    ):
        with pytest.raises(ValidationException):
            validate_video_extraction_range(2.0, 1.0, 1.0)

    def test_validate_video_extraction_range_where_start_second_greater_than_stop_second(
        self,
    ):
        with pytest.raises(ValidationException):
            validate_video_extraction_range(2.0, 1.0, 3.0)

    # valid_capture_rate
    def test_valid_capture_rate_where_capture_rate_greater_than_frame_range_from_non_terminal(
        self,
    ):
        with pytest.raises(ValidationException):
            valid_capture_rate(1, 1, 1)

    def test_valid_capture_rate_where_capture_rate_greater_than_frame_range_from_non_terminal(
        self,
    ):
        with pytest.raises(ValidationException):
            valid_capture_rate(100_000_000, 0, 30)
