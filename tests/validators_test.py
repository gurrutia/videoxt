import argparse

import pytest

import videoxt.constants as C
from videoxt.validators import ValidationException, positive_int


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


class TestNonTerminal:
    C.IS_TERMINAL = False

    def test_positive_int_with_zero_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_int(0)
        with pytest.raises(ValidationException):
            positive_int("0")

    def test_positive_int_with_negative_ints_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_int(-1)
        with pytest.raises(ValidationException):
            positive_int("-1")

    def test_positive_int_with_non_ints_from_non_terminal(self):
        with pytest.raises(ValidationException):
            positive_int("a")
        with pytest.raises(ValidationException):
            positive_int("1a")

    def test_positive_int_with_invalid_floats_from_non_terminal_1_1(self):
        with pytest.raises(ValidationException):
            positive_int(1.1)

    def test_positive_int_with_invalid_floats_from_non_terminal_0_9(self):
        with pytest.raises(ValidationException):
            positive_int(0.9)

    def test_positive_int_with_valid_floats_from_non_terminal_1_1_string(self):
        with pytest.raises(ValidationException):
            positive_int("1.1")

    def test_positive_int_with_valid_floats_from_non_terminal_0_9_string(self):
        with pytest.raises(ValidationException):
            positive_int("0.9")
