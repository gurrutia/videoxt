"""
Command line interface for the VideoXT library.

Usage:
-----
```sh
$ videoxt --help
usage: videoxt [-h] [--version] {audio,clip,frames,gif} ...

Extract audio, individual frames, short clips and GIFs from videos.

positional arguments:
  {audio,clip,frames,gif}
    audio               Extract audio from a video file.
    clip                Extract a short clip from a video file as `mp4`.
    frames              Extract individual frames from a video and save them as images.
    gif                 Create a GIF from a video between two specified points.

options:
  -h, --help            show this help message and exit
  --version, -V         show program's version number and exit
```
"""
import argparse
from collections.abc import Sequence
from functools import partial
from typing import Any

import videoxt.api
import videoxt.validators as V
from videoxt.constants import (
    SUPPORTED_AUDIO_FORMATS,
    SUPPORTED_IMAGE_FORMATS,
    VALID_ROTATE_VALUES,
    VERSION,
)
from videoxt.exceptions import VideoXTError


def split_cli_args(args: argparse.Namespace) -> tuple[str, str, dict[str, Any]]:
    """
    Split the arguments into a tuple containing the extraction method, filepath, and
    extraction options. The extraction method is determined by the subparser name,
    which can be one of either "audio", "clip", "frames", or "gif".

    Args:
    -----
        `args` (argparse.Namespace): The arguments from the CLI.

    Returns:
    -----
        `tuple[str, str, dict[str, Any]]`:
            The extraction method, filepath, and extraction options.
    """
    options = {
        k: v for k, v in vars(args).items() if k not in ["subparser_name", "filepath"]
    }

    return args.subparser_name, args.filepath, options


def execute_extraction(
    method: str,
    filepath: str,
    **options: dict[str, Any],
) -> int:
    """
    Trigger the extraction procedure and return the exit code (0 means success).

    Args:
    -----
        `method` (str]):
            The extraction method to use ("audio", "clip", "frames", "gif").
        `filepath` (str):
            Path to the video file.
        `**options` (dict):
            Extraction options specific to the chosen extraction method.

    Returns:
    -----
        `int` : 0 if the extraction was successful, 1 otherwise.
    """

    try:
        videoxt.api.extract(method, filepath, skip_validation=True, **options)
    except VideoXTError as error_msg:
        print(error_msg)
        return 1
    else:
        return 0


def main(argv: Sequence[str] | None = None) -> int:
    """
    The main entry point when called from the command-line. By default, `verbose` mode
    is enabled, which prints details about the prepared extraction request and the
    result. To disable this output, use the `--quiet` or `-q` flag.

    Args:
    -----
        `argv` (Sequence[str] | None): The arguments from the CLI.

    Returns:
    -----
        `int`: 0 if the extraction was successful, 1 otherwise.
    """
    # parent_parser houses arguments common to all subparsers
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "filepath",
        type=partial(V.valid_filepath, is_video=True),
        help="Path to the video file with extension.",
    )
    parent_parser.add_argument(
        "--start-time",
        "-s",
        type=V.valid_start_time,
        default=0,
        metavar="",
        dest="start_time",
        help=(
            "Time to start extraction. Can be a number representing seconds or a "
            "timestamp (Ex: --start-time 0:45 or -s 45)."
        ),
    )
    parent_parser.add_argument(
        "--stop-time",
        "-S",
        type=V.valid_stop_time,
        metavar="",
        dest="stop_time",
        help=(
            "Time to stop extraction. Can be a number representing seconds or a "
            "timestamp (Ex: --stop-time 1:30 or -S 90)."
        ),
    )
    parent_parser.add_argument(
        "--destdir",
        "-d",
        type=V.valid_dir,
        metavar="",
        dest="destdir",
        help=(
            "Specify the directory you want to save output to. If not provided, "
            "media is saved in the directory of the input video file."
        ),
    )
    parent_parser.add_argument(
        "--filename",
        "-fn",
        type=V.valid_filename,
        metavar="",
        dest="filename",
        help=(
            "Set the name of the output media file(s), without the extension. "
            "If not provided, the video's filename is used."
        ),
    )
    parent_parser.add_argument(
        "--quiet",
        "-q",
        action="store_false",
        dest="verbose",
        help="Disable extraction details from being printed to the console.",
    )
    parent_parser.add_argument(
        "--overwrite",
        "-ov",
        action="store_true",
        dest="overwrite",
        help="Overwrite the output file(s) if they already exist.",
    )
    parent_parser.add_argument(
        "--fps",
        "-f",
        type=V.valid_fps,
        metavar="",
        help=(
            "Manually set the video's frames per second (FPS). "
            "Helpful if the FPS is not read accurately by OpenCV. Use with caution."
        ),
    )

    # parent_parser_audio houses arguments common to audio and clip subparsers
    parent_parser_audio = argparse.ArgumentParser(add_help=False)
    parent_parser_audio.add_argument(
        "--volume",
        "-v",
        type=V.valid_volume,
        default=1.0,
        metavar="",
        help="Increase or decrease the output audio volume by a factor of N.",
    )
    parent_parser_audio.add_argument(
        "--normalize",
        action="store_true",
        help="Normalize the audio output to a maximum of 0dB.",
    )

    # parent_parser_image houses arguments common to clip, frames and gif subparsers
    parent_parser_image = argparse.ArgumentParser(add_help=False)
    parent_parser_image.add_argument(
        "--dimensions",
        "-dm",
        type=V.valid_dimensions_str,
        metavar="",
        help="Resize the output to a specific width and height (Ex: -dm 1920x1080).",
    )
    parent_parser_image.add_argument(
        "--resize",
        "-rs",
        type=V.valid_resize,
        default=1.0,
        metavar="",
        help="Increase or decrease the dimensions of the output by a factor of N.",
    )
    parent_parser_image.add_argument(
        "--rotate",
        "-rt",
        type=V.valid_rotate_value,
        choices=VALID_ROTATE_VALUES,
        default=0,
        metavar="",
        dest="rotate",
        help="Rotate the output by 90, 180, or 270 degrees.",
    )
    parent_parser_image.add_argument(
        "--monochrome",
        action="store_true",
        help="Apply a black-and-white filter to the output.",
    )

    # parent_parser_motion houses arguments common to audio, clip and gif subparsers
    parent_parser_motion = argparse.ArgumentParser(add_help=False)
    parent_parser_motion.add_argument(
        "--speed",
        "-sp",
        type=V.valid_speed,
        default=1.0,
        metavar="",
        help="Increase or decrease the speed of the output by a factor of N.",
    )
    parent_parser_motion.add_argument(
        "--bounce",
        action="store_true",
        help="Make the output bounce back-and-forth, boomerang style.",
    )
    parent_parser_motion.add_argument(
        "--reverse",
        action="store_true",
        help="Reverse the output.",
    )

    # main_parser encompasses all subparsers
    main_parser = argparse.ArgumentParser(
        prog="videoxt",
        description=(
            "Extract audio, individual frames, short clips and GIFs from videos."
        ),
    )
    main_parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    subparsers = main_parser.add_subparsers(dest="subparser_name", required=True)

    # audio subparser
    subparser_audio = subparsers.add_parser(
        "audio",
        help="Extract audio from a video file.",
        parents=[parent_parser, parent_parser_audio, parent_parser_motion],
    )
    subparser_audio.add_argument(
        "--audio-format",
        "-af",
        type=V.valid_audio_format,
        choices=SUPPORTED_AUDIO_FORMATS,
        default="mp3",
        metavar="",
        dest="audio_format",
        help="Set the extracted audio file format. Default is 'mp3'.",
    )

    # clip subparser
    subparsers.add_parser(
        "clip",
        help="Extract a short clip from a video file as 'mp4'.",
        parents=[
            parent_parser,
            parent_parser_audio,
            parent_parser_image,
            parent_parser_motion,
        ],
    )

    # frames subparser
    subparser_frames = subparsers.add_parser(
        "frames",
        help="Extract individual frames from a video and save them as images.",
        parents=[parent_parser, parent_parser_image],
    )
    subparser_frames.add_argument(
        "--image-format",
        "-if",
        type=V.valid_image_format,
        choices=SUPPORTED_IMAGE_FORMATS,
        default="jpg",
        metavar="",
        dest="image_format",
        help="Set the image format to save the frames as. Default is 'jpg'.",
    )
    subparser_frames.add_argument(
        "--capture-rate",
        "-cr",
        type=V.valid_capture_rate,
        default=1,
        metavar="",
        dest="capture_rate",
        help="Capture every Nth video frame. Default is 1, which captures every frame.",
    )

    # gif subparser
    subparsers.add_parser(
        "gif",
        help="Create a GIF from a video between two specified points.",
        parents=[parent_parser, parent_parser_image, parent_parser_motion],
    )

    # Parse the arguments and execute the extraction.
    try:
        args = main_parser.parse_args(argv)
    except (argparse.ArgumentTypeError, VideoXTError) as error_msg:
        print(error_msg)
        return 1
    else:
        method, filepath, options = split_cli_args(args)
        return execute_extraction(method, filepath, **options)


if __name__ == "__main__":
    exit(main())
