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
import videoxt.utils as U
from videoxt.requestors import AudioRequest
from videoxt.requestors import BaseRequest
from videoxt.requestors import ClipRequest
from videoxt.requestors import FramesRequest
from videoxt.requestors import GifRequest
from videoxt.video import Video


@dataclass
class Extractor(ABC):
    request: BaseRequest

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
    request: AudioRequest

    def apply_edits(self, clip: VideoFileClip) -> VideoFileClip:
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


@dataclass
class ClipExtractor(Extractor):
    request: ClipRequest

    def apply_edits(self, clip: VideoFileClip) -> VideoFileClip:
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


@dataclass
class FramesExtractor(Extractor):
    request: FramesRequest

    def apply_edits(self, image: np.ndarray) -> np.ndarray:
        return E.edit_image(
            image, self.request.dimensions, self.request.rotate, self.request.monochrome
        )

    def extract(self) -> None:
        video_capture = cv2.VideoCapture(str(self.request.video.filepath))
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.request.time_range.start_frame)

        if not self.request.destdir.exists():
            self.request.destdir.mkdir()

        if self.request.verbose:
            print(self.request.video.__str__() + str(self.request))

        with Progress(transient=True) as progress:
            task = progress.add_task(
                "EXTRACTING FRAMES", total=self.request.images_expected
            )

            frame_numbers = itertools.count(
                start=self.request.time_range.start_frame,
                step=self.request.capture_rate,
            )

            images_written = 0

            for frame_number in frame_numbers:
                read_successful, image = video_capture.read()

                if not read_successful:
                    break

                image_filepath = P.prepare_filepath_image(
                    self.request.dir,
                    self.request.filename,
                    frame_number,
                    self.request.image_format,
                )
                image = self.apply_edits(image)
                cv2.imwrite(image_filepath, image)

                images_written += 1

                progress.update(
                    task,
                    advance=1,
                    description=(
                        f"[yellow]EXTRACTING FRAMES FROM {self.request.video.filepath.name!r} "
                        f"[{images_written}/{self.request.images_expected}][/yellow]"
                    ),
                )

                if images_written == self.request.images_expected:
                    break

        video_capture.release()

        print(f"[green]FRAMES EXTRACTED: {self.request.destdir.resolve()}[/green]")


@dataclass
class GifExtractor(Extractor):
    request: GifRequest

    def apply_edits(self, clip: VideoFileClip) -> VideoFileClip:
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


def extraction_factory(
    filepath: Path,
    request_cls: t.Type[BaseRequest],
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
