import argparse

import pytest

import videoxt.constants as C
from videoxt.validators import non_negative_int
from videoxt.validators import positive_float
from videoxt.validators import positive_int
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

    def test_positive_int_with_non_int_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_int("a")

    def test_positive_int_with_invalid_float_from_non_terminal_1_1(self):
        with pytest.raises(ValidationException):
            positive_int(1.1)

    def test_positive_int_with_invalid_float_from_non_terminal_0_9(self):
        with pytest.raises(ValidationException):
            positive_int(0.9)

    def test_positive_int_with_invalid_float_string_from_non_terminal_1_1_string(self):
        with pytest.raises(ValidationException):
            positive_int("1.1")

    def test_positive_int_with_invalid_float_string_from_non_terminal_0_9_string(self):
        with pytest.raises(ValidationException):
            positive_int("0.9")

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

    def test_non_negative_int_with_negative_int_from_non_terminal(self):
        with pytest.raises(ValidationException):
            non_negative_int(-1)

    # non_negative_int
    def test_non_negative_int_with_negative_int_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            non_negative_int("-1")

    def test_non_negative_int_with_non_int_string_from_non_terminal(self):
        with pytest.raises(ValidationException):
            non_negative_int("a")

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
