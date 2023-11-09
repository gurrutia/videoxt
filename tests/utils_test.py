import json
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

import pytest

from videoxt.constants import ExtractionMethod
from videoxt.exceptions import ValidationError
from videoxt.utils import (
    CustomJSONEncoder,
    ToJsonMixin,
    append_enumeration,
    calculate_duration,
    convert_bytes,
    enumerate_dir,
    enumerate_filepath,
    parse_kwargs,
    seconds_to_timestamp,
    timedelta_to_timestamp,
    timestamp_to_seconds,
)


def test_timestamp_to_seconds_valid_input():
    """
    Test that the function returns a valid number of seconds for a given timestamp.
    """
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
    """
    Test that the function returns a valid number of seconds for an abnormal timestamp.

    The following timestamps are not valid according to the function's docstring, but
    they should be treated be handled by the function.
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
    """
    Test that the function raises a ValueError if the input is not a valid timestamp.
    """
    with pytest.raises(ValueError):
        timestamp_to_seconds("invalid")


def test_timestamp_to_seconds_empty_string():
    """Test that the function raises a ValueError if the input is an empty string."""
    with pytest.raises(ValueError):
        timestamp_to_seconds("")


def test_seconds_to_timestamp_valid_input():
    """
    Test that the function returns a valid timestamp string for a given number of
    seconds.
    """
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
    expected_path = tmp_path.with_name(f"{tmp_path.name}_vxt")
    assert enumerate_dir(tmp_path, tag="_vxt") == expected_path


def test_enumerate_dir_new_dir(tmp_path: Path):
    """Test that the same directory path is returned if the directory does not exist.

    `tmp_path` is a built-in pytest fixture that creates a temporary directory.
    """
    expected_path = tmp_path / "new_dir"
    assert enumerate_dir(expected_path) == expected_path


def test_enumerate_filepath_existing_file(fixture_tmp_text_filepath: Path):
    """Test that the filepath is enumerated if the file already exists."""
    stem = fixture_tmp_text_filepath.stem
    suffix = fixture_tmp_text_filepath.suffix
    expected_path = fixture_tmp_text_filepath.with_name(f"{stem}_vxt{suffix}")
    assert enumerate_filepath(fixture_tmp_text_filepath, tag="_vxt") == expected_path


def test_enumerate_filepath_new_file(fixture_tmp_text_filepath: Path):
    """Test that the same filepath is returned if the file does not exist."""
    expected_path = fixture_tmp_text_filepath.with_name("new_file.txt")
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
        # Test case 2: all kwargs are defined as fields in the `Image` dataclass except
        # `extra_field`.
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
        # Test case 7: one of one kwarg is not defined as a field in the `Image`
        # dataclass.
        (
            {"extra_field": ""},
            {},
        ),
        # Test case 8: empty kwargs passed.
        (
            {},
            {},
        ),
        # Test case 9: all kwargs are defined as fields in the `Image` dataclass, but
        # one is None.
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


def test_append_enumeration_when_only_index_is_entered():
    assert append_enumeration(1) == " (1)"
    assert append_enumeration(2) == " (2)"
    assert append_enumeration(3) == " (3)"


def test_append_enumeration_when_index_and_tag_are_entered():
    assert append_enumeration(1, tag="_vxt") == "_vxt"
    assert append_enumeration(2, tag="_vxt") == "_vxt (2)"
    assert append_enumeration(3, tag="_vxt") == "_vxt (3)"


def test_append_enumeration_when_index_is_0():
    assert append_enumeration(0) == " (1)"
    assert append_enumeration(0, tag="_vxt") == "_vxt"


def test_append_enumeration_when_index_is_negative():
    assert append_enumeration(-1) == " (1)"
    assert append_enumeration(-2) == " (1)"
    assert append_enumeration(-3) == " (1)"
    assert append_enumeration(-1, tag="_vxt") == "_vxt"


def test_calculate_duration_with_valid_inputs():
    frame_count = 120
    fps = 30.0
    expected_duration = timedelta(seconds=frame_count / fps)
    result = calculate_duration(frame_count, fps)
    assert result == expected_duration


def test_calculate_duration_with_negative_frame_count_should_raise_validation_error():
    with pytest.raises(ValidationError):
        calculate_duration(-120, 30.0)


def test_calculate_duration_with_frame_count_zero_should_raise_validation_error():
    with pytest.raises(ValidationError):
        calculate_duration(0, 30.0)


def test_calculate_duration_with_frame_count_point_five_should_raise_validation_error():
    with pytest.raises(ValidationError):
        calculate_duration(0.5, 30.0)


def test_calculate_duration_with_negative_fps_should_raise_validation_error():
    with pytest.raises(ValidationError):
        calculate_duration(120, -30.0)


def test_calculate_duration_with_fps_zero_should_raise_validation_error():
    with pytest.raises(ValidationError):
        calculate_duration(120, 0.0)


def test_timedelta_to_timestamp_with_zero_seconds():
    duration = timedelta(seconds=0)
    result = timedelta_to_timestamp(duration)
    assert result == "00:00:00"


def test_timedelta_to_timestamp_with_59_seconds():
    duration = timedelta(seconds=59)
    result = timedelta_to_timestamp(duration)
    assert result == "00:00:59"


def test_timedelta_to_timestamp_with_61_seconds():
    duration = timedelta(seconds=61)
    result = timedelta_to_timestamp(duration)
    assert result == "00:01:01"


def test_timedelta_to_timestamp_with_microseconds_should_truncate():
    duration = timedelta(seconds=61.123456)
    result = timedelta_to_timestamp(duration)
    assert result == "00:01:01"


def test_timedelta_to_timestamp_with_negative_duration_should_raise_value_error():
    with pytest.raises(ValueError) as exc_info:
        duration = timedelta(seconds=-1)
        timedelta_to_timestamp(duration)
    assert "Invalid duration: timedelta must be non-negative" in str(exc_info.value)


def test_convert_bytes_with_bytes():
    bytes_ = 1024
    result = convert_bytes(bytes_)
    assert result == "1.00 KB"


def test_convert_bytes_with_kilobytes():
    kilobytes = 1024**2
    result = convert_bytes(kilobytes)
    assert result == "1.00 MB"


def test_convert_bytes_with_megabytes():
    megabytes = 1024**3
    result = convert_bytes(megabytes)
    assert result == "1.00 GB"


def test_convert_bytes_with_gigabytes():
    gigabytes = 1024**4
    result = convert_bytes(gigabytes)
    assert result == "1.00 TB"


def test_convert_bytes_with_terabytes():
    terabytes = 1024**5
    result = convert_bytes(terabytes)
    assert result == "1.00 PB"


def test_convert_bytes_with_negative_bytes_should_raise_value_error():
    with pytest.raises(ValidationError) as exc_info:
        bytes_ = -1024
        convert_bytes(bytes_)
    assert "Expected positive integer" in str(exc_info.value)


def test_custom_json_encoder_encode_path():
    path_obj = Path("/path/to/file")
    encoded_path = json.dumps(path_obj, cls=CustomJSONEncoder)
    expected_path = path_obj.resolve().as_posix()
    assert encoded_path == json.dumps(expected_path)


def test_custom_json_encoder_encode_timedelta():
    duration = timedelta(hours=1, minutes=11)
    encoded_duration = json.dumps(duration, cls=CustomJSONEncoder)
    assert encoded_duration == '"1:11:00"'


def test_custom_json_encoder_encode_extraction_method_enum():
    encoded_method = json.dumps(ExtractionMethod.AUDIO, cls=CustomJSONEncoder)
    assert encoded_method == '"audio"'
    encoded_method = json.dumps(ExtractionMethod.CLIP, cls=CustomJSONEncoder)
    assert encoded_method == '"clip"'
    encoded_method = json.dumps(ExtractionMethod.FRAMES, cls=CustomJSONEncoder)
    assert encoded_method == '"frames"'
    encoded_method = json.dumps(ExtractionMethod.GIF, cls=CustomJSONEncoder)
    assert encoded_method == '"gif"'


def test_custom_json_encoder_unhandled_custom_object_raises_type_error():
    class UnhandledCustomObject:
        pass

    with pytest.raises(TypeError):
        json.dumps(UnhandledCustomObject(), cls=CustomJSONEncoder)


def test_to_json_mixin_to_json_skip_private_keys_is_false():
    @dataclass
    class TestClass(ToJsonMixin):
        a: str
        b: int
        _private: bool = True

    test_obj = TestClass("c", 4)
    expected_json = '{\n  "a": "c",\n  "b": 4,\n  "_private": true\n}'
    assert test_obj.json(skip_private_keys=False) == expected_json


def test_to_json_mixin_to_json_skip_private_keys_is_true():
    @dataclass
    class TestClass(ToJsonMixin):
        a: str
        b: int
        _private: bool = True

    test_obj = TestClass("c", 4)
    expected_json = '{\n  "a": "c",\n  "b": 4\n}'
    assert test_obj.json(skip_private_keys=True) == expected_json
