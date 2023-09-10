"""Extractor objects that implement video extraction using Request objects."""
import itertools
import typing as t
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path

import cv2  # type: ignore
import numpy as np
from moviepy.editor import VideoFileClip  # type: ignore
from rich import print
from rich.console import Console
from rich.progress import Progress

import videoxt.editors as E
import videoxt.preppers as P
import videoxt.requestors as R
import videoxt.utils as U
from videoxt.video import Video


@dataclass
class Extractor(ABC):
    """Abstract class for all extractors. All extractors adhere to this interface."""

    request: R.BaseRequest
    success: bool = False

    @abstractmethod
    def apply_edits(
        self, clip: t.Union[VideoFileClip, np.ndarray]
    ) -> t.Union[VideoFileClip, np.ndarray]:
        """Perform edits to the output media prior to extraction."""
        pass

    @abstractmethod
    def extract(self) -> Path:
        """Initiate and perform the extraction process. Returns the path to
        the extracted media.

        Returns:
            Path: The path to the extracted media.
        """
        pass


@dataclass
class AudioExtractor(Extractor):
    """Applies edits to a VideoFileClip and extracts the audio from the clip."""

    request: R.AudioRequest

    def apply_edits(self, clip: VideoFileClip) -> VideoFileClip:
        """Apply edits to the clip prior to audio extraction.

        Args:
            clip (VideoFileClip): The clip to edit.

        Returns:
            VideoFileClip: The edited clip.
        """
        clip = E.trim_clip(
            clip,
            self.request.time_range.start_second,
            self.request.time_range.stop_second,
        )
        clip = E.edit_clip_audio(clip, self.request.volume, self.request.normalize)
        clip = E.edit_clip_motion(
            clip, self.request.speed, self.request.reverse, self.request.bounce
        )

        return clip

    def extract(self) -> Path:
        """Extract audio from a video and save to a file.

        Returns:
            Path: The path to the extracted audio file.
        """
        with VideoFileClip(str(self.request.video.filepath)) as clip:
            if not clip.audio:
                raise ValueError(
                    f"Video {self.request.video.filepath.name!r} does not have audio."
                )

            subclip = self.apply_edits(clip)

            if self.request.verbose:
                print(self.request.video.__str__() + str(self.request))

            with Console().status(
                f"[yellow]EXTRACTING AUDIO FROM {self.request.video.filepath.name!r} "
                f"TO {self.request.filepath.name!r}[/yellow]"
            ):
                subclip.audio.write_audiofile(
                    str(self.request.filepath), logger=None, fps=44100
                )

            print(
                f"[green]AUDIO EXTRACTED: {str(self.request.filepath.resolve())}[/green]"
            )

        self.success = True
        return self.request.filepath


@dataclass
class ClipExtractor(Extractor):
    """Applies edits to a VideoFileClip and extracts the clip."""

    request: R.ClipRequest

    def apply_edits(self, clip: VideoFileClip) -> VideoFileClip:
        """Apply edits to a VideoFileClip to create a subclip.

        Args:
            clip (VideoFileClip): The clip to edit.

        Returns:
            VideoFileClip: The edited clip.
        """
        clip = E.trim_clip(
            clip,
            self.request.time_range.start_second,
            self.request.time_range.stop_second,
        )
        clip = E.edit_clip_audio(clip, self.request.volume, self.request.normalize)
        clip = E.edit_clip_motion(
            clip, self.request.speed, self.request.reverse, self.request.bounce
        )
        clip = E.edit_clip_image(
            clip, self.request.dimensions, self.request.rotate, self.request.monochrome
        )

        return clip

    def extract(self) -> Path:
        """Extract a subclip from a video and save it to disk.

        Returns:
            Path: The path to the extracted clip.
        """
        with VideoFileClip(str(self.request.video.filepath)) as clip:
            subclip = self.apply_edits(clip)

            if self.request.verbose:
                print(self.request.video.__str__() + str(self.request))

            with Console().status(
                f"[yellow]EXTRACTING CLIP FROM {self.request.video.filepath.name!r} "
                f"TO {self.request.filepath.name!r}[/yellow]"
            ):
                subclip.write_videofile(str(self.request.filepath), logger=None)

            print(
                f"[green]CLIP EXTRACTED: {str(self.request.filepath.resolve())}[/green]"
            )

        self.success = True
        return self.request.filepath


@dataclass
class FramesExtractor(Extractor):
    """Applies edits to an image `numpy.ndarray` and extracts the frames."""

    request: R.FramesRequest

    def apply_edits(self, image: np.ndarray) -> np.ndarray:
        """Apply edits to an image `numpy.ndarray`.

        Args:
            image (np.ndarray): The image to edit.

        Returns:
            np.ndarray: The edited image.
        """
        return E.edit_image(
            image, self.request.dimensions, self.request.rotate, self.request.monochrome
        )

    def extract(self) -> Path:
        """Extract frames from a video and save them to a directory as images.

        Returns:
            Path: The directory where the images were saved.
        """
        if not self.request.destdir.exists():
            self.request.destdir.mkdir()

        if self.request.verbose:
            print(self.request.video.__str__() + str(self.request))

        with Progress(transient=True) as progress:
            task = progress.add_task(
                "EXTRACTING FRAMES",
                total=self.request.images_expected,
            )

            images_written = 0
            frame_queue = itertools.count(
                start=self.request.time_range.start_frame,
                step=self.request.capture_rate,
            )
            for frame_num in frame_queue:
                with self.request.video.open_capture() as opencap:
                    opencap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                    read_successful, image = opencap.read()

                    if not read_successful:
                        break

                    # Generate the filepath for the next image to be written
                    image_filepath = P.prepare_filepath_image(
                        self.request.destdir,
                        self.request.filename,
                        frame_num,
                        self.request.image_format,
                    )
                    image = self.apply_edits(image)
                    cv2.imwrite(image_filepath, image)
                    images_written += 1

                    # Update progress bar
                    progress.update(
                        task,
                        advance=1,
                        description=(
                            f"[yellow]EXTRACTING FRAMES FROM "
                            f"{self.request.video.filepath.name!r} "
                            f"[{images_written}/{self.request.images_expected}]"
                            f"[/yellow]"
                        ),
                    )

                    if images_written == self.request.images_expected:
                        break

        print(f"[green]FRAMES EXTRACTED: {self.request.destdir.resolve()}[/green]")

        self.success = True
        return self.request.destdir


@dataclass
class GifExtractor(Extractor):
    """Applies edits to a VideoFileClip and extracts the gif from the clip."""

    request: R.GifRequest

    def apply_edits(self, clip: VideoFileClip) -> VideoFileClip:
        """Apply edits to a clip and return the edited clip for gif extraction.

        Args:
            clip (VideoFileClip): The clip to edit.

        Returns:
            VideoFileClip: The edited clip.
        """
        clip = E.trim_clip(
            clip,
            self.request.time_range.start_second,
            self.request.time_range.stop_second,
        )
        clip = E.edit_clip_image(
            clip, self.request.dimensions, self.request.rotate, self.request.monochrome
        )
        clip = E.edit_clip_motion(
            clip, self.request.speed, self.request.reverse, self.request.bounce
        )

        return clip

    def extract(self) -> Path:
        """Extract a gif from a video and save it to disk.

        Returns:
            Path: The path to the extracted gif.
        """
        with VideoFileClip(str(self.request.video.filepath)) as clip:
            subclip = self.apply_edits(clip)

            if self.request.verbose:
                print(self.request.video.__str__() + str(self.request))

            with Console().status(
                f"[yellow]EXTRACTING GIF FROM {self.request.video.filepath.name!r} "
                f"TO {self.request.filepath.name!r}[/yellow]"
            ):
                subclip.write_gif(str(self.request.filepath), logger=None)

            print(
                f"[green]GIF EXTRACTED: {str(self.request.filepath.resolve())}[/green]"
            )

        self.success = True
        return self.request.filepath


def extraction_factory(
    filepath: Path,
    request_cls: t.Type[R.BaseRequest],
    extractor_cls: t.Type[Extractor],
    **kwargs: t.Dict[str, t.Any],
) -> t.Type[Extractor]:
    """Creates instances of a Video object, a Request object, and an Extractor
    object to extract data from a Video object. The Request and Extractor
    objects should be of the same type (e.g. `FramesRequest` and `FramesExtractor`)

    Args:
        `filepath` (Path, str) :
            Path to the video file with extension.
        `request_cls` (Type[Request]) :
            The type of `Request` object to create.
        `extractor_cls` (Type[Extractor]) :
            The type of `Extractor` object to create.
        `**kwargs` (Dict[str, Any]) :
            Keyword arguments to pass to the `Request` object.

    Returns:
        Extractor: An instance of an `Extractor` object.
    """
    video = Video(filepath)
    request_kwargs = U.parse_kwargs(kwargs, request_cls) if kwargs else kwargs
    request = request_cls(video, **request_kwargs)
    extractor = extractor_cls(request)
    extractor.extract()

    return extractor
