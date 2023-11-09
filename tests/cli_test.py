import argparse

from videoxt.cli import split_cli_args


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
