import argparse
import shutil

import pytest

from videoxt.cli import execute_extraction, main, split_cli_args


def test_split_cli_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser_name")
    subparser = subparsers.add_parser("audio")
    subparser.add_argument("filepath")
    subparser.add_argument("--option1")
    subparser.add_argument("--option2")

    args = parser.parse_args(["audio", "input_file.mp4", "--option1", "value1"])

    extraction_method, filepath, options = split_cli_args(args)

    assert extraction_method == "audio"
    assert filepath == "input_file.mp4"
    assert options == {"option1": "value1", "option2": None}


def test_execute_extraction_returns_exit_code_0_for_valid_video_file(
    fixture_tmp_video_filepath,
):
    destdir = fixture_tmp_video_filepath.parent
    filename = "tmp.execute.extraction.audio"
    destpath = destdir / f"{filename}.mp3"
    exit_code = execute_extraction(
        method="audio",  # quickest extraction method
        filepath=str(fixture_tmp_video_filepath),
        **{"destdir": destdir, "filename": filename},
    )
    assert exit_code == 0
    assert destpath.exists()

    try:
        destpath.unlink()
    except FileNotFoundError:
        pass


def test_execute_extraction_returns_exit_code_1_for_invalid_video_file(
    fixture_tmp_video_filepath_zero_seconds,
):
    exit_code = execute_extraction(
        method="audio",
        filepath=str(fixture_tmp_video_filepath_zero_seconds),
        **{},
    )
    assert exit_code == 1


@pytest.mark.parametrize(
    "method, suffix", [("audio", "mp3"), ("clip", "mp4"), ("gif", "gif")]
)
def test_main_successful_extraction_returns_exit_code_0(
    fixture_tmp_video_filepath, method, suffix
):
    destdir = fixture_tmp_video_filepath.parent
    filename = "tmp.main.successful.extraction"
    destpath = destdir / f"{filename}.{suffix}"
    exit_code = main(
        [
            method,
            str(fixture_tmp_video_filepath),
            "--filename",
            filename,
            "--destdir",
            str(destdir),
        ]
    )
    assert exit_code == 0
    assert destpath.exists()

    try:
        destpath.unlink()
    except FileNotFoundError:
        pass


def test_main_successful_frames_extraction_returns_exit_code_0(
    fixture_tmp_video_filepath,
):
    destdir = fixture_tmp_video_filepath.parent / "frames"
    destdir.mkdir(parents=True, exist_ok=True)
    exit_code = main(
        [
            "frames",
            str(fixture_tmp_video_filepath),
            "--destdir",
            str(destdir),
        ]
    )
    assert exit_code == 0
    assert destdir.exists()

    try:
        shutil.rmtree(destdir)
    except FileNotFoundError:
        pass


def test_main_with_invalid_positional_arg_raises_argparse_argument_error_and_returns_exit_code_1(
    fixture_tmp_video_filepath,
):
    with pytest.raises(SystemExit):
        exit_code = main(["invalid_positional_arg", str(fixture_tmp_video_filepath)])
        assert exit_code == 0


@pytest.mark.parametrize("method", ["audio", "clip", "frames", "gif"])
def test_main_with_invalid_video_file_returns_exit_code_1(
    fixture_tmp_video_filepath_zero_seconds, method
):
    exit_code = main([method, str(fixture_tmp_video_filepath_zero_seconds)])
    assert exit_code == 1


@pytest.mark.parametrize("method", ["audio", "clip", "frames", "gif"])
def test_main_with_unrecognized_option_returns_exit_code_1(
    fixture_tmp_video_filepath, method
):
    with pytest.raises(SystemExit):
        exit_code = main([method, str(fixture_tmp_video_filepath), "--invalid_option"])
        assert exit_code == 1


@pytest.mark.parametrize("method", ["audio", "clip", "frames", "gif"])
def test_main_argument_type_error_returns_exit_code_1(
    fixture_tmp_video_filepath, method
):
    exit_code = main([method, str(fixture_tmp_video_filepath), "--start-time", "-1"])
    assert exit_code == 1


@pytest.mark.parametrize("method", ["audio", "clip", "frames", "gif"])
def test_main_videoxt_error_returns_exit_code_1(fixture_tmp_video_filepath, method):
    exit_code = main(
        [
            method,
            str(fixture_tmp_video_filepath),
            "--start-time",
            "2",
            "--stop-time",
            "1",
        ]
    )
    assert exit_code == 1
