import datetime
import math
import os
from dataclasses import dataclass, field
from textwrap import dedent
from typing import Optional, Tuple, Union

import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate, vfx
from rich import print
from rich.console import Console
from rich.progress import Progress

import videoxt.constants as C
import videoxt.utils as utils
import videoxt.validators as V


@dataclass
class BaseVideoExtractor:
    video_path: str
    start_time: Union[float, int, str] = 0.0
    stop_time: Optional[Union[float, int, str]] = None
    fps: Optional[float] = None
    dimensions: Optional[Tuple[int, int]] = None
    resize: float = 1.0
    rotate: int = 0
    output_dir: Optional[str] = None
    output_filename: Optional[str] = None
    quiet: bool = False
    emoji: bool = False
    extraction_type: str = field(init=False)
    start_second: float = field(init=False)
    stop_second: float = field(init=False)
    start_frame: float = field(init=False)
    stop_frame: float = field(init=False)
    target_dimensions: Tuple[int, int] = field(init=False)
    frame_count: float = field(init=False)
    video_abspath: str = field(init=False)
    video_basename: str = field(init=False)
    video_dirname: str = field(init=False)
    video_filename: str = field(init=False)
    video_length: str = field(init=False)
    video_length_seconds: float = field(init=False)
    video_dimensions: Tuple[int, int] = field(init=False)

    def __post_init__(self) -> None:
        """The order in which these methods are called is important."""
        self.extraction_type = self.__class__.__name__.lower().replace("videoto", "")
        self._validate_user_input()
        self._initialize_video_attributes()
        self._initialize_video_metadata()
        self._set_video_extraction_seconds_range()
        V.validate_video_extraction_range(
            self.start_second, self.stop_second, self.video_length_seconds
        )
        self._set_video_extraction_frame_range()
        self._set_default_output_dir()
        self._set_default_output_filename()
        self._set_target_dimensions()

    def _validate_user_input(self) -> None:
        """Validations when run from command-line are handled by argparse."""
        if not C.IS_TERMINAL:
            self.video_path = V.valid_filepath(self.video_path)
            self.start_time = V.valid_start_time(self.start_time)
            self.stop_time = (
                V.valid_stop_time(self.stop_time)
                if self.stop_time is not None
                else self.stop_time
            )
            self.fps = V.positive_float(self.fps) if self.fps is not None else None
            self.resize = V.valid_resize_value(self.resize)
            self.dimensions = (
                V.valid_dimensions(self.dimensions)
                if self.dimensions is not None
                else self.dimensions
            )
            self.rotate = V.valid_rotate_value(self.rotate)
            self.output_dir = (
                V.valid_dir(self.output_dir)
                if self.output_dir is not None
                else self.output_dir
            )
            if self.output_filename is not None:
                self.output_filename = V.valid_filename(self.output_filename)

    def _initialize_video_attributes(self) -> None:
        self.video_abspath = (
            self.video_path
            if os.path.isabs(self.video_path)
            else os.path.abspath(self.video_path)
        )
        self.video_dirname = os.path.dirname(self.video_abspath)
        self.video_basename = os.path.basename(self.video_abspath)
        self.video_filename = os.path.splitext(self.video_basename)[0]

    def _initialize_video_metadata(self) -> None:
        """Video metadata initialized: frame count, fps, video length, and video dimensions."""
        video_capture = cv2.VideoCapture(self.video_abspath)

        self.frame_count = round(video_capture.get(cv2.CAP_PROP_FRAME_COUNT), 2)

        if self.fps is None:
            self.fps = round(video_capture.get(cv2.CAP_PROP_FPS), 2)

        self.video_length_seconds = round(self.frame_count / self.fps, 2)
        self.video_length = utils.seconds_to_timestamp(self.video_length_seconds)

        self.video_dimensions = (
            int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )

        video_capture.release()

    def _set_video_extraction_seconds_range(self) -> None:
        """Set the start and stop seconds for video extraction

        The stop second is set to the video length if the stop time is not specified or
        if the stop second is greater than the video length.
        """
        self.start_second = (
            utils.timestamp_to_seconds(self.start_time)
            if isinstance(self.start_time, str)
            else self.start_time
        )

        if self.stop_time is not None:
            self.stop_second = (
                utils.timestamp_to_seconds(self.stop_time)
                if isinstance(self.stop_time, str)
                else self.stop_time
            )
            self.stop_second = (
                self.video_length_seconds
                if self.stop_second > self.video_length_seconds
                else self.stop_second
            )
        else:
            self.stop_second = self.video_length_seconds

    def _set_video_extraction_frame_range(self) -> None:
        """Set the start and stop frame for video extraction

        The stop frame is set to the frame count if the stop time is not specified or
        if the stop frame is greater than the frame count.
        """
        self.start_frame = round(self.start_second * self.fps, 2)

        if self.stop_time is not None:
            self.stop_frame = round(self.stop_second * self.fps, 2)
            self.stop_frame = (
                self.frame_count
                if self.stop_frame > self.frame_count
                else self.stop_frame
            )
        else:
            self.stop_frame = self.frame_count

    def _set_default_output_dir(self) -> None:
        """Set the default output directory for extracted frames or gif.

        For the 'images' extraction type:
        If the output directory is not specified, the default directory will be created
        in the same directory as the video file. If the default directory already exists,
        a new directory will be created with a number appended to the end of the name.

        For the 'gif' extraction type:
        If the output directory is not specified, the gif will be saved in the same directory
        as the video file.
        """
        if self.extraction_type == "images":
            if self.output_dir is None:
                output_dir_name = f"{self.video_filename}_frames"
                output_dir = os.path.join(self.video_dirname, output_dir_name)

                if os.path.exists(output_dir):
                    index = 2
                    while os.path.exists(output_dir):
                        output_dir = os.path.join(
                            self.video_dirname, f"{output_dir_name} ({index})"
                        )
                        index += 1

                self.output_dir = output_dir

        elif self.extraction_type == "gif":
            if self.output_dir is None:
                self.output_dir = self.video_dirname

    def _set_default_output_filename(self) -> None:
        """Set the default output filename for extracted frames or gif.

        For the 'images' extraction type:
        If the output filename is not specified, the default filename will be the name of the video file
        with '_frame' appended to the end.

        For the 'gif' extraction type:
        If the output filename is not specified, the default filename will be the name of the video file
        with '.gif' appended to the end. If the output filename is specified, the '.gif' extension will be
        appended to the end of the filename if it is not already present.
        """
        if self.extraction_type == "images":
            if self.output_filename is None:
                self.output_filename = f"{self.video_filename}_frame"

        elif self.extraction_type == "gif":
            if self.output_filename is None:
                self.output_filename = f"{self.video_filename}.gif"
            else:
                if not self.output_filename.endswith(".gif"):
                    self.output_filename += ".gif"

    def _set_target_dimensions(self) -> None:
        """Set the target dimensions for extracted frames or gif.

        If the resize value is not 1, each dimension will be multiplied by the resize value,
        regardless of whether or not the user specified the dimensions.
        If the user does not specify the dimensions, the target dimensions
        will be the same as the video dimensions.
        """
        if self.dimensions is not None:
            if self.resize != 1:
                self.target_dimensions = tuple(
                    [int(dimension * self.resize) for dimension in self.dimensions]
                )
            else:
                self.target_dimensions = self.dimensions
        else:
            if self.resize != 1:
                self.target_dimensions = tuple(
                    [
                        int(dimension * self.resize)
                        for dimension in self.video_dimensions
                    ]
                )
            else:
                self.target_dimensions = self.video_dimensions

    def __str__(self) -> str:
        start_time_display = f"{utils.seconds_to_timestamp(self.start_second)} | {self.start_second} seconds"
        stop_time_display = f"{utils.seconds_to_timestamp(self.stop_second)} | {self.stop_second} seconds"
        if self.emoji:
            start_time_display = f"{C.EMOJI_MAP['start']} {start_time_display}"
            stop_time_display = f"{C.EMOJI_MAP['stop']} {stop_time_display}"

        return dedent(
            f"""
            {'VIDEO' if not self.emoji else C.EMOJI_MAP['video']}
              input:        {self.video_path!r}
              length:       {self.video_length} | {self.video_length_seconds} seconds
              fps:          {self.fps}
              frame count:  {self.frame_count}
              dimensions:   {self.video_dimensions}
            {'EXTRACTION' if not self.emoji else C.EMOJI_MAP['extraction']}
              type:         {self.extraction_type!r}
              start time:   {start_time_display}
              stop time:    {stop_time_display}
              start frame:  {self.start_frame + 1 if not self.emoji else C.EMOJI_MAP['start'] + ' ' + str(self.start_frame + 1)}
              stop frame:   {self.stop_frame + 1 if not self.emoji else C.EMOJI_MAP['stop'] + ' ' + str(self.stop_frame + 1)}
              output dir:   {self.output_dir}"""
        )


@dataclass
class VideoToImages(BaseVideoExtractor):
    capture_rate: int = 1
    image_format: str = "jpg"
    images_expected: int = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self._validate_image_input()
        self._set_images_expected()

    def _validate_image_input(self) -> None:
        if not C.IS_TERMINAL:
            self.image_format = V.valid_image_format(self.image_format)
            self.capture_rate = V.positive_int(self.capture_rate)

        self.capture_rate = V.valid_capture_rate(
            self.capture_rate, self.start_frame, self.stop_frame
        )

    def _set_images_expected(self) -> None:
        self.images_expected = math.ceil(
            (self.stop_frame - self.start_frame) / self.capture_rate
        )

    def _apply_image_transformations(self, image: np.ndarray) -> np.ndarray:
        image = cv2.resize(image, self.target_dimensions)

        if self.rotate in C.ROTATION_MAP:
            image = cv2.rotate(image, C.ROTATION_MAP[self.rotate])

        return image

    def extract_images(self) -> None:
        video_capture = cv2.VideoCapture(self.video_path)
        frame_position = int(self.start_frame)
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_position)

        # Only creates the directory if the default output directory `video_frames_*.jpg` was used.
        if not os.path.exists(str(self.output_dir)):
            os.mkdir(str(self.output_dir))

        if not self.quiet:
            print(str(self))

        with Progress(transient=True) as progress:
            extract_task = progress.add_task(
                f"[yellow]EXTRACTING FRAMES {self.video_basename}",
                total=self.images_expected,
            )

            images_written = 1
            while video_capture.isOpened():
                read_successful, image = video_capture.read()
                if read_successful:
                    # Write image to disk,
                    image_filename = f"{self.output_filename}_{frame_position + 1}.{self.image_format}"
                    image_path = os.path.join(str(self.output_dir), image_filename)
                    image = self._apply_image_transformations(image)
                    cv2.imwrite(image_path, image)

                    if self.images_expected == images_written:
                        video_capture.release()
                        break

                    # cv2.VideoCapture.read() increments and sets the next frame position by 1 on next read.
                    # Therefore, the frame position is incremented by the capture rate only if capture rate > 1.
                    frame_position += self.capture_rate
                    if self.capture_rate != 1:
                        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_position)

                    progress.update(
                        extract_task,
                        advance=1,
                        description=f"[yellow]EXTRACTING FRAMES FROM {self.video_basename!r} [{images_written}/{self.images_expected}]",
                    )

                    images_written += 1

                else:
                    video_capture.release()
                    break

        print(
            f"[green]EXTRACTION COMPLETE [{images_written}] IMAGES SAVED: {self.output_dir}[/green]"
        )

    def __str__(self) -> str:
        if self.emoji:
            if self.resize < 1:
                resize_display = str(self.resize) + " " + C.EMOJI_MAP["resize_small"]
            elif self.resize > 1:
                resize_display = str(self.resize) + " " + C.EMOJI_MAP["resize_large"]
            else:
                resize_display = str(self.resize) + " " + C.EMOJI_MAP["resize_normal"]

            rotate_display = str(self.rotate) + " " + C.EMOJI_MAP[self.rotate]
        else:
            resize_display = str(self.resize)
            rotate_display = str(self.rotate)

        name_display = f"{self.output_filename}_*.{self.image_format}"

        return super().__str__() + dedent(
            f"""
            {"IMAGES" if not self.emoji else C.EMOJI_MAP['image']}
              filenames:    {name_display!r}
              format:       {self.image_format!r}
              resize:       {resize_display}
              rotate:       {rotate_display}
              capture rate: {self.capture_rate}
              expected:     {self.images_expected}
              dimensions:   {self.target_dimensions}
              """
        )


@dataclass
class VideoToGIF(BaseVideoExtractor):
    speed: float = 1.0
    bounce: bool = False

    def __post_init__(self) -> None:
        super().__post_init__()
        self._validate_gif_input()

    def _validate_gif_input(self) -> None:
        if not C.IS_TERMINAL:
            self.speed = V.positive_float(self.speed)

    def _apply_gif_transformations(self, subclip: VideoFileClip) -> VideoFileClip:
        subclip = subclip.resize(self.target_dimensions).speedx(self.speed)

        if self.rotate != 0:
            subclip = subclip.rotate(self.rotate)

        if self.bounce:
            subclip = concatenate([subclip, subclip.fx(vfx.time_mirror)])

        return subclip

    def create_gif(self) -> None:
        with VideoFileClip(self.video_path, audio=False) as clip:
            # Create a subclip of the video from start_second to stop_second and apply transformations.
            subclip = clip.subclip(self.start_second, self.stop_second)
            subclip = self._apply_gif_transformations(subclip)

            gif_path = os.path.join(str(self.output_dir), str(self.output_filename))

            if not self.quiet:
                print(str(self))

            with Console().status(
                f"[yellow]CREATING GIF {self.output_filename!r} FROM {self.video_basename!r}[/yellow]"
            ):
                subclip.write_gif(
                    gif_path,
                    fps=self.fps,
                    logger=None,
                )
            print(f"[green]GIF CREATED HERE: {gif_path}[/green]")

    def __str__(self) -> str:
        if self.emoji:
            if self.resize < 1:
                resize_display = str(self.resize) + " " + C.EMOJI_MAP["resize_small"]
            elif self.resize > 1:
                resize_display = str(self.resize) + " " + C.EMOJI_MAP["resize_large"]
            else:
                resize_display = str(self.resize) + " " + C.EMOJI_MAP["resize_normal"]

            rotate_display = str(self.rotate) + " " + C.EMOJI_MAP[self.rotate]

            if self.speed > 1:
                speed_display = str(self.speed) + " " + C.EMOJI_MAP["speed_fast"]
            elif self.speed < 1:
                speed_display = str(self.speed) + " " + C.EMOJI_MAP["speed_slow"]
            else:
                speed_display = str(self.speed) + " " + C.EMOJI_MAP["speed_normal"]
        else:
            resize_display = str(self.resize)
            rotate_display = str(self.rotate)
            speed_display = str(self.speed)

        return super().__str__() + dedent(
            f"""
            {"GIF" if not self.emoji else C.EMOJI_MAP['gif']}
              filename:     {self.output_filename!r}
              resize:       {resize_display}
              rotate:       {rotate_display}
              speed:        {speed_display}
              bounce:       {self.bounce}
              dimensions:   {self.target_dimensions}
              """
        )
