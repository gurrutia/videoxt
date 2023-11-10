import argparse

from videoxt.cli import execute_extraction, split_cli_args


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
