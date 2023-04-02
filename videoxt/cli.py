import argparse
import sys
import typing as t

import videoxt.api as API
import videoxt.constants as C
import videoxt.validators as V
from videoxt.exceptions import ValidationException


def process_args(args: argparse.Namespace) -> int:
    """Process the arguments from the CLI.

    Args:
    ------------
    `args` (argparse.Namespace) :
        The arguments from the CLI.

    Returns:
    ------------
        `int` :
            `0` if successful, `1` if not.
    """
    subparser_name = args.subparser_name
    del args.subparser_name

    filepath = args.filepath
    del args.filepath

    kwargs = vars(args)

    if subparser_name == "audio":
        API.extract_audio(filepath, **kwargs)
        return 0
    elif subparser_name == "clip":
        API.extract_clip(filepath, **kwargs)
        return 0
    elif subparser_name == "frames":
        API.extract_frames(filepath, **kwargs)
        return 0
    elif subparser_name == "gif":
        API.extract_gif(filepath, **kwargs)
        return 0

    return 1


def main(argv: t.Optional[t.Sequence[str]] = None) -> int:
    """The main entry point for the CLI."""

    # parent_parser houses arguments common to all subparsers
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "filepath",
        type=V.valid_filepath_cli,
        help="Path to the video file with extension.",
    )
    parent_parser.add_argument(
        "--start-time",
        "-s",
        type=V.valid_start_time_cli,
        default="0:00:00",
        metavar="",
        dest="start_time",
        help="Time to start extraction. Can be a number representing seconds or a timestamp (Ex: --start-time 0:45 or -s 45).",
    )
    parent_parser.add_argument(
        "--stop-time",
        "-S",
        type=V.valid_stop_time_cli,
        metavar="",
        dest="stop_time",
        help="Time to stop extraction. Can be a number representing seconds or a timestamp (Ex: --stop-time 1:30 or -S 90).",
    )
    parent_parser.add_argument(
        "--fps",
        "-f",
        type=V.positive_float_cli,
        metavar="",
        help="Manually set the frames per second (FPS). Helpful if the FPS is not read accurately.",
    )
    parent_parser.add_argument(
        "--destdir",
        "-d",
        type=V.valid_dir_cli,
        metavar="",
        dest="destdir",
        help="Specify the directory you want to save the media to. If not provided, media is saved in the video directory.",
    )
    parent_parser.add_argument(
        "--filename",
        "-fn",
        type=V.valid_filename_cli,
        metavar="",
        dest="filename",
        help="Set the name of the output media file(s), without the extension. If not provided, the video filename is used.",
    )
    parent_parser.add_argument(
        "--quiet",
        "-q",
        action="store_false",
        dest="verbose",
        help="Disable extraction details from being printed to the console.",
    )

    # parent_parser_audio houses arguments common to audio and clip subparsers
    parent_parser_audio = argparse.ArgumentParser(add_help=False)
    parent_parser_audio.add_argument(
        "--volume",
        "-v",
        type=V.non_negative_float_cli,
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
        type=V.positive_int_cli,
        nargs=2,
        metavar="",
        help="Resize the output to a specific width and height (Ex: --dm 1920 1080).",
    )
    parent_parser_image.add_argument(
        "--resize",
        "-rs",
        type=V.valid_resize_value_cli,
        default=1.0,
        metavar="",
        help="Increase or decrease the dimensions of the output by a factor of N.",
    )
    parent_parser_image.add_argument(
        "--rotate",
        "-rt",
        type=V.valid_rotate_value_cli,
        default=0,
        metavar="",
        dest="rotate",
        help="Rotate the output by 90, 180, or 270 degrees.",
    )
    parent_parser_image.add_argument(
        "--monochrome",
        action="store_true",
        help="Apply a black and white filter to the output.",
    )

    # parent_parser_motion houses arguments common to audio, clip and gif subparsers
    parent_parser_motion = argparse.ArgumentParser(add_help=False)
    parent_parser_motion.add_argument(
        "--speed",
        "-sp",
        type=V.positive_float_cli,
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
        description="Extract audio, clips, frames and create gifs from a video.",
    )
    main_parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"%(prog)s {C.VERSION}",
    )
    subparsers = main_parser.add_subparsers(dest="subparser_name", required=True)

    # audio subparser
    subparser_audio = subparsers.add_parser(
        "audio",
        help="Extract audio from video.",
        parents=[parent_parser, parent_parser_audio],
    )
    subparser_audio.add_argument(
        "--audio-format",
        "-af",
        type=V.valid_audio_format_cli,
        metavar="",
        default="mp3",
        dest="audio_format",
        help="Set the audio format to as. Default is 'mp3'.",
    )

    # clip subparser
    subparsers.add_parser(
        "clip",
        help="Extract a clip of a video file. Only supports 'mp4' output.",
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
        type=V.valid_image_format_cli,
        metavar="",
        default="jpg",
        dest="image_format",
        help="Set the image format to save the frames as. Default is 'jpg'.",
    )
    subparser_frames.add_argument(
        "--capture-rate",
        "-cr",
        type=V.positive_int_cli,
        default=1,
        metavar="",
        dest="capture_rate",
        help="Capture every Nth video frame. Default is 1, which captures every frame.",
    )

    # gif subparser
    subparsers.add_parser(
        "gif",
        help="Create a GIF between two points in a video.",
        parents=[parent_parser, parent_parser_image, parent_parser_motion],
    )

    try:
        args = main_parser.parse_args(argv)
    except argparse.ArgumentTypeError as e:
        print(e)
        return 1

    try:
        return process_args(args)
    except ValidationException as e:
        print(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
