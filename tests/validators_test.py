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
