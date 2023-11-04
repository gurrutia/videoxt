from pathlib import Path

import pytest

import videoxt.constants as C
from videoxt.exceptions import ValidationError
from videoxt.validators import (
    non_negative_float,
    non_negative_int,
    positive_float,
    positive_int,
    valid_audio_format,
    valid_dimensions,
    valid_dir,
    valid_extraction_range,
    valid_filename,
    valid_filepath,
    valid_image_format,
    valid_rotate_value,
    valid_start_time,
    valid_stop_time,
    valid_timestamp,
    valid_video_file_suffix,
    valid_volume,
)


def test_positive_int_valid_int():
    assert positive_int(42) == 42


def test_positive_int_valid_string():
    assert positive_int("42") == 42


def test_positive_int_valid_float():
    assert positive_int(42.0) == 42


def test_positive_int_valid_float_string():
    assert positive_int("42.0") == 42


def test_positive_int_zero_int():
    with pytest.raises(ValidationError):
        positive_int(0)


def test_positive_int_zero_int_string():
    with pytest.raises(ValidationError):
        positive_int("0")


def test_positive_int_zero_float():
    with pytest.raises(ValidationError):
        positive_int(0.0)


def test_positive_int_negative_int():
    with pytest.raises(ValidationError):
        positive_int(-42)


def test_positive_int_negative_int_string():
    with pytest.raises(ValidationError):
        positive_int("-42")


def test_positive_int_negative_float():
    with pytest.raises(ValidationError):
        positive_int(-42.0)


def test_positive_int_negative_float_string():
    with pytest.raises(ValidationError):
        positive_int("-42.0")


def test_positive_int_invalid_float():
    with pytest.raises(ValidationError):
        positive_int(42.5)


def test_positive_int_invalid_float_string():
    with pytest.raises(ValidationError):
        positive_int("42.5")


def test_positive_int_invalid_string():
    with pytest.raises(ValidationError):
        positive_int("abc")


def test_positive_int_empty_string():
    with pytest.raises(ValidationError):
        positive_int("")


def test_positive_int_none():
    with pytest.raises(ValidationError):
        positive_int(None)


def test_positive_float_valid_float():
    assert positive_float(3.14) == 3.14


def test_positive_float_valid_float_string():
    assert positive_float("3.14") == 3.14


def test_positive_float_valid_int():
    assert positive_float(42) == 42.0


def test_positive_float_valid_int_string():
    assert positive_float("42") == 42.0


def test_positive_float_negative_float():
    with pytest.raises(ValidationError):
        positive_float(-3.14)


def test_positive_float_negative_float_string():
    with pytest.raises(ValidationError):
        positive_float("-3.14")


def test_positive_float_negative_int():
    with pytest.raises(ValidationError):
        positive_float(-42)


def test_positive_float_negative_int_string():
    with pytest.raises(ValidationError):
        positive_float("-42")


def test_positive_float_zero_float():
    with pytest.raises(ValidationError):
        positive_float(0.0)


def test_positive_float_zero_float_string():
    with pytest.raises(ValidationError):
        positive_float("0.0")


def test_positive_float_zero_int():
    with pytest.raises(ValidationError):
        positive_float(0)


def test_positive_float_zero_int_string():
    with pytest.raises(ValidationError):
        positive_float("0")


def test_positive_float_invalid_string():
    with pytest.raises(ValidationError):
        positive_float("abc")


def test_positive_float_empty_string():
    with pytest.raises(ValidationError):
        positive_float("")


def test_positive_float_none():
    with pytest.raises(ValidationError):
        positive_float(None)


def test_non_negative_int_valid():
    assert non_negative_int(42) == 42


def test_non_negative_int_valid_string():
    assert non_negative_int("42") == 42


def test_non_negative_int_valid_float():
    assert non_negative_int(42.0) == 42


def test_non_negative_int_valid_float_string():
    assert non_negative_int("42.0") == 42


def test_non_negative_int_zero_int():
    assert non_negative_int(0) == 0


def test_non_negative_int_zero_int_string():
    assert non_negative_int("0") == 0


def test_non_negative_int_zero_float():
    assert non_negative_int(0.0) == 0


def test_non_negative_int_negative_int():
    with pytest.raises(ValidationError):
        non_negative_int(-42)


def test_non_negative_int_negative_int_string():
    with pytest.raises(ValidationError):
        non_negative_int("-42")


def test_non_negative_int_negative_float():
    with pytest.raises(ValidationError):
        non_negative_int(-42.0)


def test_non_negative_int_negative_float_string():
    with pytest.raises(ValidationError):
        non_negative_int("-42.0")


def test_non_negative_int_invalid_float():
    with pytest.raises(ValidationError):
        non_negative_int(42.5)


def test_non_negative_int_invalid_float_string():
    with pytest.raises(ValidationError):
        non_negative_int("42.5")


def test_non_negative_int_invalid_string():
    with pytest.raises(ValidationError):
        non_negative_int("abc")


def test_non_negative_int_empty_string():
    with pytest.raises(ValidationError):
        non_negative_int("")


def test_non_negative_int_none():
    with pytest.raises(ValidationError):
        non_negative_int(None)


def test_non_negative_float_valid_float():
    assert non_negative_float(3.14) == 3.14


def test_non_negative_float_valid_float_string():
    assert non_negative_float("3.14") == 3.14


def test_non_negative_float_valid_int():
    assert non_negative_float(42) == 42.0


def test_non_negative_float_valid_int_string():
    assert non_negative_float("42") == 42.0


def test_non_negative_float_zero_float():
    assert non_negative_float(0.0) == 0.0


def test_non_negative_float_zero_float_string():
    assert non_negative_float("0.0") == 0.0


def test_non_negative_float_zero_int():
    assert non_negative_float(0) == 0.0


def test_non_negative_float_zero_int_string():
    assert non_negative_float("0") == 0.0


def test_non_negative_float_negative_float():
    with pytest.raises(ValidationError):
        non_negative_float(-3.14)


def test_non_negative_float_negative_float_string():
    with pytest.raises(ValidationError):
        non_negative_float("-3.14")


def test_non_negative_float_negative_int():
    with pytest.raises(ValidationError):
        non_negative_float(-42)


def test_non_negative_float_negative_int_string():
    with pytest.raises(ValidationError):
        non_negative_float("-42")


def test_non_negative_float_invalid_string():
    with pytest.raises(ValidationError):
        non_negative_float("abc")


def test_non_negative_float_empty_string():
    with pytest.raises(ValidationError):
        non_negative_float("")


def test_non_negative_float_none():
    with pytest.raises(ValidationError):
        non_negative_float(None)


def test_valid_filepath_valid_path(fixture_tmp_video_filepath: Path):
    assert valid_filepath(fixture_tmp_video_filepath) == fixture_tmp_video_filepath


def test_valid_filepath_valid_string(fixture_tmp_video_filepath: Path):
    assert valid_filepath(str(fixture_tmp_video_filepath)) == fixture_tmp_video_filepath


def test_valid_filepath_nonexistent_path():
    path = Path("nonexistent") / "file.mp4"
    with pytest.raises(ValidationError):
        valid_filepath(path)


def test_valid_filepath_nonexistent_string():
    path = "nonexistent/file.mp4"
    with pytest.raises(ValidationError):
        valid_filepath(path)


def test_valid_filepath_none():
    with pytest.raises(ValidationError):
        valid_filepath(None)


def test_valid_image_format_valid_image_formats():
    for image_format in C.SUPPORTED_IMAGE_FORMATS:
        assert valid_image_format(image_format) == image_format


def test_valid_image_format_valid_image_formats_uppercase():
    for image_format in C.SUPPORTED_IMAGE_FORMATS:
        assert valid_image_format(image_format.upper()) == image_format


def test_valid_image_format_valid_image_formats_start_with_dot():
    for image_format in C.SUPPORTED_IMAGE_FORMATS:
        assert valid_image_format(f".{image_format}") == image_format


def test_valid_image_format_invalid_image_formats_end_with_dot():
    for image_format in C.SUPPORTED_IMAGE_FORMATS:
        with pytest.raises(ValidationError):
            valid_image_format(f"{image_format}.")


def test_valid_image_format_invalid_image_format():
    with pytest.raises(ValidationError):
        valid_image_format("invalid")


def test_valid_image_format_invalid_empty_string():
    with pytest.raises(ValidationError):
        valid_image_format("")


def test_valid_dir_valid_path(tmp_path: Path):
    assert valid_dir(tmp_path) == tmp_path


def test_valid_dir_valid_string(tmp_path: Path):
    assert valid_dir(str(tmp_path)) == tmp_path


def test_valid_dir_with_dot_as_path_returns_cwd():
    assert valid_dir(Path(".")) == Path().cwd()


def test_valid_dir_with_dot_as_string_returns_cwd():
    assert valid_dir(".") == Path().cwd()


def test_valid_dir_with_two_dots_as_path_returns_parent_dir():
    assert valid_dir(Path("..")) == Path().cwd().parent


def test_valid_dir_with_two_dots_as_string_returns_parent_dir():
    assert valid_dir("..") == Path().cwd().parent


def test_valid_dir_valid_path_with_trailing_slash(tmp_path: Path):
    assert valid_dir(tmp_path / "") == tmp_path


def test_valid_dir_valid_string_with_trailing_slash(tmp_path: Path):
    assert valid_dir(str(tmp_path / "")) == tmp_path


def test_valid_dir_invalid_path(tmp_path: Path):
    with pytest.raises(ValidationError):
        valid_dir(tmp_path / "invalid")


def test_valid_dir_invalid_string(tmp_path: Path):
    with pytest.raises(ValidationError):
        valid_dir(str(tmp_path / "invalid"))


def test_valid_dir_with_forward_slash():
    with pytest.raises(ValidationError):
        valid_dir("/")


def test_valid_dir_none():
    with pytest.raises(ValidationError):
        valid_dir(None)


@pytest.mark.parametrize(
    ("start", "stop", "duration", "expected"),
    [
        (0, 1, 2, (0, 1, 2)),  # start < stop < duration
        (1, 3, 3, (1, 3, 3)),  # stop < stop, stop == duration
    ],
)
def test_valid_extraction_range_valid_range(
    start: float, stop: float, duration: float, expected: tuple[float, float, float]
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
    with pytest.raises(ValidationError):
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
    assert valid_filename(filename) == expected_filename


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
    with pytest.raises(ValidationError):
        valid_filename(filename)


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
    assert valid_timestamp(timestamp) == expected


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
    with pytest.raises(ValidationError):
        valid_timestamp(timestamp)


def test_valid_audio_format_valid_audio_formats():
    for audio_format in C.SUPPORTED_AUDIO_FORMATS:
        assert valid_audio_format(audio_format) == audio_format


def test_valid_audio_format_valid_audio_formats_uppercase():
    for audio_format in C.SUPPORTED_AUDIO_FORMATS:
        assert valid_audio_format(audio_format.upper()) == audio_format


def test_valid_audio_format_valid_audio_formats_start_with_dot():
    for audio_format in C.SUPPORTED_AUDIO_FORMATS:
        assert valid_audio_format(f".{audio_format}") == audio_format


def test_valid_audio_format_invalid_audio_formats_end_with_dot():
    for audio_format in C.SUPPORTED_AUDIO_FORMATS:
        with pytest.raises(ValidationError):
            valid_audio_format(f"{audio_format}.")


def test_valid_audio_format_invalid_audio_format():
    with pytest.raises(ValidationError):
        valid_audio_format("invalid")


def test_valid_audio_format_invalid_empty_string():
    with pytest.raises(ValidationError):
        valid_audio_format("")


@pytest.mark.parametrize(
    ("dimensions", "expected"),
    [
        ((1, 2), (1, 2)),  # width < height
        ((2, 1), (2, 1)),  # width > height
        ((1, 1), (1, 1)),  # width == height
        ((1.0, 1.0), (1, 1)),  # whole float
        (("1", "1"), (1, 1)),  # integer as string
        (("1.0", "1.0"), (1, 1)),  # whole float as string
    ],
)
def test_valid_dimensions_valid_dimensions(
    dimensions: tuple[int, int], expected: tuple[int, int]
):
    assert valid_dimensions(dimensions) == expected


@pytest.mark.parametrize(
    ("dimensions"),
    [
        ((-1, -1)),  # width or height cannot be negative
        ((0, 0)),  # width or height cannot be (0)
        ((1, 2, 3)),  # dimensions cannot have more than two values
        ((1,)),  # dimensions cannot have less than two values
        (()),  # dimensions cannot be empty
        ((1.5, 1.5)),  # dimensions cannot be floating point values
        (("1.5", "1.5")),  # dimensions cannot be floating point values as strings
        (("abc", "abc")),  # dimensions cannot be strings
    ],
)
def test_valid_dimensions_invalid_dimensions(dimensions: tuple[int, int]):
    with pytest.raises(ValidationError):
        valid_dimensions(dimensions)


def test_valid_rotate_value_valid_rotate_ints():
    for rotate_value in C.VALID_ROTATE_VALUES:
        assert valid_rotate_value(rotate_value) == rotate_value


def test_valid_rotate_value_valid_rotate_floats():
    for rotate_value in C.VALID_ROTATE_VALUES:
        assert valid_rotate_value(float(rotate_value)) == rotate_value


def test_valid_rotate_value_valid_rotate_int_strings():
    for rotate_value in C.VALID_ROTATE_VALUES:
        assert valid_rotate_value(str(rotate_value)) == rotate_value


@pytest.mark.parametrize(
    ("rotate_value"),
    [
        ("0.0"),
        ("90.0"),
        ("180.0"),
        ("270.0"),
        (-1),
        ("-1"),
        (-1.0),
        ("-1.0"),
        (42),
        ("42"),
        (42.0),
        ("42.0"),
        ("abc"),
        (""),
    ],
)
def test_valid_rotate_value_invalid_rotate_values(rotate_value: float | int | str):
    with pytest.raises(ValidationError):
        valid_rotate_value(rotate_value)


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
    fixture_tmp_video_filepath,
):
    assert (
        valid_filepath(fixture_tmp_video_filepath, is_video=True)
        == fixture_tmp_video_filepath
    )


def test_valid_video_filepath_with_supported_existing_filepath_string(
    fixture_tmp_video_filepath,
):
    path_str = str(fixture_tmp_video_filepath)
    assert valid_filepath(path_str, is_video=True) == fixture_tmp_video_filepath


def test_valid_video_filepath_with_supported_existing_filepath_lowercase_suffix(
    fixture_tmp_video_filepath,
):
    path = fixture_tmp_video_filepath.with_suffix(".mp4")
    assert valid_filepath(path, is_video=True) == fixture_tmp_video_filepath


def test_valid_video_filepath_with_supported_nonexistant_video_filepath(tmp_path: Path):
    path = tmp_path / "t.mp4"
    with pytest.raises(ValidationError):
        valid_filepath(path, is_video=True)


def test_valid_video_filepath_with_supported_nonexistant_video_filepath_string():
    with pytest.raises(ValidationError):
        valid_filepath("t.mp4", is_video=True)


def test_valid_video_filepath_with_unsupported_existing_file_suffix(
    fixture_tmp_text_filepath,
):
    with pytest.raises(ValidationError):
        valid_filepath(fixture_tmp_text_filepath, is_video=True)


def test_valid_video_filepath_with_unsupported_nonexistant_file_suffix():
    with pytest.raises(ValidationError):
        valid_filepath("t.txt", is_video=True)


def test_valid_video_filepath_with_directory_path(tmp_path: Path):
    with pytest.raises(ValidationError):
        valid_filepath(tmp_path, is_video=True)


def test_valid_video_file_suffix_with_supported_video_file_suffixes():
    for suffix in C.SUPPORTED_VIDEO_FORMATS:
        assert valid_video_file_suffix(suffix) == suffix


def test_valid_video_file_suffix_with_uppercase_supported_video_file_suffixes():
    for suffix in C.SUPPORTED_VIDEO_FORMATS:
        assert valid_video_file_suffix(suffix.upper()) == suffix


def test_valid_video_file_suffix_with_supported_video_file_suffixes_start_with_dot():
    for suffix in C.SUPPORTED_VIDEO_FORMATS:
        assert valid_video_file_suffix(f".{suffix}") == suffix


def test_valid_video_file_suffix_with_unsupported_video_file_suffix():
    with pytest.raises(ValidationError):
        valid_video_file_suffix(".abc")


def test_valid_volume_with_valid_volume():
    assert valid_volume(-1) == 0.0
    assert valid_volume(0.0) == 0.0
    assert valid_volume(0.5) == 0.5
    assert valid_volume(1.0) == 1.0
    assert valid_volume(1.5) == 1.5
    assert valid_volume("2") == 2.0
    assert valid_volume("3.0") == 3.0


def test_valid_volume_with_invalid_input():
    with pytest.raises(ValidationError):
        valid_volume("abc")
    with pytest.raises(ValidationError):
        valid_volume(None)
    with pytest.raises(ValidationError):
        valid_volume("")
    with pytest.raises(ValidationError):
        valid_volume(" ")
