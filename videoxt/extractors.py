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
    def extract(self) -> None:
        """Initiate the extraction process."""
        pass


@dataclass
class AudioExtractor(Extractor):
    """Applies edits to a VideoFileClip and extracts the audio from the clip."""

    request: R.AudioRequest

    def apply_edits(self, clip: VideoFileClip) -> VideoFileClip:
        """Apply edits to the clip prior to audio extraction."""
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

    def extract(self) -> None:
        """Extract audio from a video and save to a file."""
        with VideoFileClip(str(self.request.video.filepath)) as clip:
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


@dataclass
class ClipExtractor(Extractor):
    """Applies edits to a VideoFileClip and extracts the clip."""

    request: R.ClipRequest

    def apply_edits(self, clip: VideoFileClip) -> VideoFileClip:
        """Apply edits to a VideoFileClip to create a subclip."""
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

    def extract(self) -> None:
        """Extract a clip from a video and save it to disk as a video."""
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


@dataclass
class FramesExtractor(Extractor):
    """Applies edits to an image `numpy.ndarray` and extracts the frames."""

    request: R.FramesRequest

    def apply_edits(self, image: np.ndarray) -> np.ndarray:
        """Apply edits to an image `numpy.ndarray`."""
        return E.edit_image(
            image, self.request.dimensions, self.request.rotate, self.request.monochrome
        )

    def extract(self) -> None:
        """Extract frames from a video and save them to a directory as images."""
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
        """Apply edits to a VideoFileClip and return the edited clip for gif extraction."""
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

    def extract(self) -> None:
        """Extract a gif from a video and save it to disk."""
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


def extraction_factory(
    filepath: Path,
    request_cls: t.Type[R.BaseRequest],
    extractor_cls: t.Type[Extractor],
    **kwargs: t.Dict[str, t.Any],
) -> None:
    """
    Factory function that creates instances of a `Video` class, a `Request` class, and
    an `Extractor` class to extract data from a `Video`.

    Args:
        filepath: A `Path` object to the video file.
        request_cls: A subclass of a `BaseRequest` class for creating an extraction request.
        extractor_cls: A subclass of an `Extractor` class that performs the extraction.
        **kwargs: Optional keyword arguments to use for creating the request.
    """
    video = Video(filepath)
    request_kwargs = U.parse_kwargs(kwargs, request_cls) if kwargs else kwargs
    request = request_cls(video, **request_kwargs)
    extractor = extractor_cls(request)
    extractor.extract()
