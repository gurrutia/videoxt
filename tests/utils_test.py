import pytest

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
