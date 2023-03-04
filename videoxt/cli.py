import argparse
import sys
from typing import Optional, Sequence

from rich import print

import videoxt.constants as C
import videoxt.validators as V
from videoxt.extractors import VideoToGIF, VideoToImages


def main(argv: Optional[Sequence[str]] = None) -> None:
    C.IS_TERMINAL = True

    # parent_parser houses shared subparser args
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "video_path",
        type=V.valid_filepath,
        help="Path to the video file with extension.",
    )
    parent_parser.add_argument(
        "--start-time",
        type=V.valid_start_time,
        default=0.0,
        metavar="",
        dest="start_time",
        help="Specify the start time of the video to extract frames from. Default is the start of the video.",
    )
    parent_parser.add_argument(
        "--stop-time",
        type=V.valid_stop_time,
        metavar="",
        dest="stop_time",
        help="Specify the stop time of the video to extract frames from. Default is the end of the video.",
    )
    parent_parser.add_argument(
        "--fps",
        type=V.positive_float,
        metavar="",
        help="Specify the video frames per second. This will override the video metadata FPS.",
    )
    parent_parser.add_argument(
        "--dimensions",
        type=V.positive_int,
        nargs=2,
        metavar="",
        help="Specify the media output dimensions as space-separated values (Ex: --dimensions 1920 1080). Defaults to native video dimensions.",
    )
    parent_parser.add_argument(
        "--resize",
        type=V.valid_resize_value,
        default=1.0,
        metavar="",
        help="Resize the media output by a factor of n. Default is 1.0, which is the original size of the video.",
    )
    parent_parser.add_argument(
        "--rotate",
        type=V.valid_rotate_value,
        default=0,
        metavar="",
        dest="rotate",
        help="Rotate the media output by 90, 180, or 270 degrees. Default is 0 (no rotation).",
    )
    parent_parser.add_argument(
        "--output-dir",
        type=V.valid_dir,
        metavar="",
        dest="output_dir",
        help="Directory to save the media output to. Default is within input video directory.",
    )
    parent_parser.add_argument(
        "--output-filename",
        type=V.valid_filename,
        metavar="",
        dest="output_filename",
        help="Specify the file name of the media output. Default is the input video file name.",
    )
    parent_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Disable extraction details in terminal.",
    )
    parent_parser.add_argument(
        "--emoji",
        action="store_true",
        help="Enable emoji's in terminal.",
    )

    # main parser and subparsers
    main_parser = argparse.ArgumentParser(
        prog="vxt",
        description="Extract individual frames from a video, or create a GIF between two points in a video.",
    )
    main_parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {C.VERSION}",
    )
    subparsers = main_parser.add_subparsers(dest="subparser_name", required=True)

    # img subparser
    parser_img = subparsers.add_parser(
        "images",
        help="Extract individual frames from a video as images.",
        parents=[parent_parser],
    )
    parser_img.add_argument(
        "--capture-rate",
        type=V.positive_int,
        default=1,
        metavar="",
        dest="capture_rate",
        help="Capture every nth video frame. Default is 1, which captures every frame.",
    )
    parser_img.add_argument(
        "--image-format",
        type=V.valid_image_format,
        default="jpg",
        metavar="",
        dest="image_format",
        help="Specify the image format to save the frames as. Default is jpg.",
    )

    # gif subparser
    parser_gif = subparsers.add_parser(
        "gif",
        help="create a GIF between two points in a video.",
        parents=[parent_parser],
    )
    parser_gif.add_argument(
        "--speed",
        type=V.positive_float,
        default=1.0,
        metavar="",
        help="Speed of the GIF animation. Default is 1.0, which is the original speed of the video.",
    )

    # parse args
    args = main_parser.parse_args(argv)

    if args.subparser_name == "images":
        try:
            vti = VideoToImages(
                video_path=args.video_path,
                start_time=args.start_time,
                stop_time=args.stop_time,
                dimensions=args.dimensions,
                resize=args.resize,
                rotate=args.rotate,
                fps=args.fps,
                output_dir=args.output_dir,
                output_filename=args.output_filename,
                quiet=args.quiet,
                emoji=args.emoji,
                capture_rate=args.capture_rate,
                image_format=args.image_format,
            )
        except argparse.ArgumentTypeError as e:
            print(e)
            sys.exit(1)
        else:
            vti.extract_images()

    if args.subparser_name == "gif":
        try:
            vtg = VideoToGIF(
                video_path=args.video_path,
                start_time=args.start_time,
                stop_time=args.stop_time,
                dimensions=args.dimensions,
                resize=args.resize,
                rotate=args.rotate,
                fps=args.fps,
                output_dir=args.output_dir,
                output_filename=args.output_filename,
                quiet=args.quiet,
                emoji=args.emoji,
                speed=args.speed,
            )
        except argparse.ArgumentTypeError as e:
            print(e)
            sys.exit(1)
        else:
            vtg.create_gif()


if __name__ == "__main__":
    main()
