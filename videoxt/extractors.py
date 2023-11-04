"""This module contains extractor objects that perform extractions."""
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import cv2  # type: ignore
import numpy as np
from moviepy.editor import VideoFileClip  # type: ignore

import videoxt.editors as E
import videoxt.requestors as R
from videoxt.exceptions import (
    AudioWriteError,
    BuildImagePathError,
    ClipWriteError,
    FrameReadError,
    FrameWriteError,
    GifWriteError,
    VideoCaptureSetError,
)
from videoxt.video import open_video_capture


class Extractor(Protocol):
    """Protocol defining the interface for performing any extraction operation."""

    def extract(self) -> Path | None:
        """
        Perform extraction and return the path to the extracted file or directory.

        Returns:
        -----
            `Path`: The path to the extracted file or directory.
        """
        ...


@dataclass
class AudioExtractor:  # XXX: Optimize.
    """
    Instantiate me with a `PreparedAudioRequest` and I'll provide you with an
    `extract()` method that will extract audio from the video file in the request,
    apply requested edits to the audio, and save it to disk.

    Fields:
    -----
        `request` (PreparedAudioRequest):
            Request parameters the extractor will use to perform the extraction.

    Public Methods:
    -----
        `extract()` -> `Path`:
            Execute audio extraction and return the path to the extracted audio
            file.
    """

    request: R.PreparedAudioRequest

    def __post_init__(self) -> None:
        """Prepare the request if it has yet to be prepared."""
        self.request = (
            self.request
            if self.request.is_prepared
            else self.request.prepare()  # XXX: log
        )

    def extract(self) -> Path:
        """
        Extract audio from a video within a given time range and return the path to the
        saved audio file. Optional edits to audio are applied before saving to disk.

        Returns:
        -----
            `Path | None`:
                The path to the extracted audio file if the write was successful.
        """
        with VideoFileClip(str(self.request.video.filepath)) as clip:
            subclip = self._edit_clip_audio(clip)
            return self._write_audio_file(subclip)

    def _edit_clip_audio(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Apply optional edits to a clip before writing to disk as an audio file.

        Args:
        -----
            `clip` (moviepy.editor.VideoFileClip): The clip to apply edits to.

        Returns:
        -----
            `moviepy.editor.VideoFileClip`: The clip with edits applied.
        """
        start: float | None = self.request.extraction_range.get("start_second", None)
        stop: float | None = self.request.extraction_range.get("stop_second", None)
        clip = E.trim_clip(clip, start, stop)

        clip = E.edit_clip_motion(
            clip, self.request.speed, self.request.reverse, self.request.bounce
        )

        clip = E.edit_clip_audio(clip, self.request.volume, self.request.normalize)

        return clip

    def _write_audio_file(self, subclip: VideoFileClip) -> Path:
        """
        Write the audio from a subclip to disk and return the path to the audio file.

        Returns:
        -----
            `Path`:
                The path to the extracted audio file if the write was successful.

        Raises:
        -----
            `AudioWriteError`:
                If the audio file could not be written to disk (from OSError).
        """
        try:
            subclip.audio.write_audiofile(
                str(self.request.destpath), logger=None, fps=44100
            )
        except OSError as e:
            raise AudioWriteError(
                f"Error writing audio to {self.request.destpath}"
            ) from e
        else:
            return self.request.destpath


@dataclass
class ClipExtractor:  # XXX: Optimize.
    """
    Instantiate me with a `PreparedClipRequest` and I'll provide you with an `extract()`
    method that will extract a subclip from the video file in the request, apply
    requested edits to the subclip, and save it to disk.

    Fields:
    -----
        `request` (PreparedClipRequest):
            Request parameters the extractor will use to perform the extraction.

    Public Methods:
    -----
        `extract()` -> `Path`:
            Execute subclip extraction and return the path to the extracted clip.
    """

    request: R.PreparedClipRequest

    def __post_init__(self) -> None:
        """Prepare the request if it has yet to be prepared."""
        self.request = (
            self.request
            if self.request.is_prepared
            else self.request.prepare()  # XXX: log
        )

    def extract(self) -> Path:
        """
        Extract a subclip from a video within a given time range and return the file
        path to clip. Optional edits to the clip are applied before saving to disk.

        Returns:
        -----
            `Path`:
                The path to the extracted clip if the write was successful.
        """
        with VideoFileClip(str(self.request.video.filepath)) as clip:
            subclip = self._edit_clip(clip)
            return self._write_subclip(subclip)

    def _edit_clip(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Apply optional edits to a clip before writing to disk as a 'mp4' file.

        Args:
        -----
            `clip` (moviepy.editor.VideoFileClip): The clip to edit.

        Returns:
        -----
            `moviepy.editor.VideoFileClip`: The edited clip.
        """
        start: float | None = self.request.extraction_range.get("start_second", None)
        stop: float | None = self.request.extraction_range.get("stop_second", None)
        clip = E.trim_clip(clip, start, stop)

        clip = E.edit_clip_audio(clip, self.request.volume, self.request.normalize)

        clip = E.edit_clip_motion(
            clip, self.request.speed, self.request.reverse, self.request.bounce
        )

        clip = E.edit_clip_image(
            clip, self.request.dimensions, self.request.rotate, self.request.monochrome
        )

        return clip

    def _write_subclip(self, subclip: VideoFileClip) -> Path:
        """
        Write a subclip to disk and return the path to the clip.

        Returns:
        -----
            `Path`:
                The path to the extracted clip if the write was successful.

        Raises:
        -----
            `ClipWriteError`: If the clip could not be written to disk (from OSError).
        """
        try:
            subclip.write_videofile(str(self.request.destpath), logger=None)
        except OSError as e:
            raise ClipWriteError(
                f"Error writing clip to {self.request.destpath}"
            ) from e
        else:
            return self.request.destpath


@dataclass
class FramesExtractor:  # XXX: Optimize.
    """
    Instantiate me with a `PreparedFramesRequest` and I'll provide you with an
    `extract()` method that will extract frames from the video file in the request,
    apply requested edits to the frames, and save them to disk as images in a directory.

    Fields:
    -----
        `request` (PreparedFramesRequest):
            The request to prepare and perform an extraction operation with.

    Public Methods:
    -----
        `extract()` -> `Path`:
            Execute frames extraction and return the path to the directory where the
            extracted images were saved.
    """

    request: R.PreparedFramesRequest

    def __post_init__(self) -> None:
        """Prepare the request if it has yet to be prepared."""
        self.request = (
            self.request
            if self.request.is_prepared
            else self.request.prepare()  # XXX: log
        )

    def extract(self) -> Path:
        """
        Extract frames from a video, save them to disk as images, and return the path
        to the directory where the images were saved.

        Returns:
        -----
            `Path`: The directory where the extracted images were saved.
        """

        # Create the destination directory if it doesn't exist.
        self.request.destpath.mkdir(parents=True, exist_ok=True)

        from rich.progress import track

        # Open the video capture and iterate over the frames to write to disk.
        with open_video_capture(self.request.video.filepath) as opencap:
            for edited_frame, image_path in track(
                self._preprocess_frames(opencap),
                total=self.request.images_expected,
                transient=True,
                description=(
                    "[yellow]Extracting frames...[/yellow]\n"
                    "Press [red][bold]Ctrl+C[/red][/bold] to cancel."
                ),
            ):
                self._write_image(edited_frame, image_path)

        return self.request.destpath

    def _preprocess_frames(
        self, opencap: cv2.VideoCapture
    ) -> Generator[tuple[np.ndarray[Any, Any], Path], None, None]:
        """
        Edit the frames to be extracted and yield the image path and the edited frame.

        Args:
        -----
            `opencap` (cv2.VideoCapture): The open video capture to read from.

        Yields:
        -----
            `tuple[Path, np.ndarray[Any, Any]]`:
                A tuple containing the image path and frame.
        """
        # Iterate over the range of frames to extract.
        for frame_num in self._generate_frame_numbers():
            # Build the image path, read video frame, apply edits, yield path and frame.
            frame = self._read_video_frame(opencap, frame_num)
            edited_frame = self._edit_video_frame(frame)
            image_path = self._build_image_path(frame_num)
            yield edited_frame, image_path

    def _generate_frame_numbers(self) -> Generator[int, None, None]:
        start_frame = self.request.extraction_range.get("start_frame", 0)
        stop_frame = self.request.extraction_range.get(
            "stop_frame", self.request.video.frame_count
        )
        capture_rate = self.request.capture_rate
        images_expected = self.request.images_expected

        current_frame = start_frame
        while current_frame < stop_frame and images_expected > 0:
            yield current_frame
            current_frame += capture_rate
            images_expected -= 1

    def _build_image_path(self, frame_num: int) -> Path:
        """
        Build the filepath for the next image to be written.

        Args:
        -----
            `frame_num` (int):The frame number to build the filepath for.

        Returns:
        -----
            `Path`: The filepath for the next image to be written.

        Raises:
        -----
            `BuildImagePathError`:
                If the destination directory or filename is None.
        """
        if self.request.destpath is None or self.request.filename is None:
            raise BuildImagePathError("The destination directory or filename is None.")

        return (
            self.request.destpath
            / f"{self.request.filename}_{frame_num+1}.{self.request.image_format}"
        )

    def _read_video_frame(
        self, opencap: cv2.VideoCapture, frame_num: int
    ) -> np.ndarray[Any, Any]:
        """
        Point the video capture to the frame number to read (0-based index) and return
        a `np.ndarray[Any, Any]` representing the video frame.

        Args:
        -----
            `opencap` (cv2.VideoCapture):
                The open video capture to read from.
            `frame_num` (int):
                The frame number to read.

        Returns:
        -----
            `np.ndarray[Any, Any]`: The video frame from the capture.

        Raises:
        -----
            `VideoCaptureSetError`:
                If opencap.set(cv2.CAP_PROP_POS_FRAMES, frame_num) returns False.
            `FrameReadError`:
                If opencap.read() could not grab, decode and return the frame.

        Notes:
        -----
            - set() uses a 0-based index of the frame to be decoded/captured next.
            - set() returns True if the capture device has accepts the property value,
            even if property value remains unchanged.
            - read() returns a tuple of (bool, np.ndarray[Any, Any]).
        """
        set_successful = opencap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        if not set_successful:
            raise VideoCaptureSetError(
                "Could not set 'cv2.CAP_PROP_POS_FRAMES' property in the video "
                f"capture to frame number {frame_num}."
            )

        read_successful: bool
        frame: np.ndarray[Any, Any]
        read_successful, frame = opencap.read()
        if not read_successful:
            raise FrameReadError(
                f"Could not read frame {frame_num} from video capture."
            )

        return frame

    def _edit_video_frame(self, frame: np.ndarray[Any, Any]) -> np.ndarray[Any, Any]:
        """
        Apply optional edits to a np.ndarray before writing to disk as an image.

        Args:
        -----
            `frame` (np.ndarray[Any, Any]): The video frame to edit.

        Returns:
        -----
            `np.ndarray[Any, Any]`: The edited video frame.
        """
        return E.edit_image(
            frame, self.request.dimensions, self.request.rotate, self.request.monochrome
        )

    def _write_image(
        self, edited_frame: np.ndarray[Any, Any], image_path: Path
    ) -> None:
        """
        Write an edited frame to disk as an image.

        Args:
        -----
            `edited_frame` (np.ndarray[Any, Any]):
                The edited video frame to write to disk as an image.
            `image_path` (Path):
                The path to write the image to.

        Raises:
        -----
            `FrameWriteError`:
            - If cv2.imwrite() raises an OSError.
            - If cv2.imwrite() returns False.
        """
        try:
            write_successful = cv2.imwrite(str(image_path), edited_frame)
        except OSError as e:
            raise FrameWriteError(f"Error writing image to {image_path}") from e
        else:
            if not write_successful:
                raise FrameWriteError(f"Unsuccessful write to {image_path}")


@dataclass
class GifExtractor:  # XXX: Optimize.
    """
    Instantiate me with a `PreparedGifRequest` and I'll provide you with an `extract()`
    method that will extract a gif from the video file in the request, apply requested
    edits to the gif, and save it to disk.

    Attributes:
    -----
        `request` (PreparedGifRequest):
            Request parameters the extractor will use to perform the extraction.

    Public Methods:
    -----
        `extract()` -> `Path`:
            Execute gif extraction and return the path to the extracted gif.
    """

    request: R.PreparedGifRequest

    def __post_init__(self) -> None:
        """Prepare the request if it has yet to be prepared."""
        self.request = (
            self.request
            if self.request.is_prepared
            else self.request.prepare()  # XXX: log
        )

    def extract(self) -> Path:
        """
        Extract a gif from a video within a given time range and return the file path
        the gif. Optional edits to the gif are applied before saving to disk.

        Returns:
        -----
            `Path`:
                The path to the extracted gif if the write was successful.
        """
        with VideoFileClip(str(self.request.video.filepath)) as clip:
            subclip = self._edit_clip(clip)
            return self._write_gif(subclip)

    def _edit_clip(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Apply optional edits to a clip.

        Args:
        -----
            `clip` (moviepy.editor.VideoFileClip): The clip to edit.

        Returns:
        -----
            `moviepy.editor.VideoFileClip`: The edited clip.
        """
        start: float | None = self.request.extraction_range.get("start_second", None)
        stop: float | None = self.request.extraction_range.get("stop_second", None)
        clip = E.trim_clip(clip, start, stop)

        clip = E.edit_clip_image(
            clip, self.request.dimensions, self.request.rotate, self.request.monochrome
        )

        clip = E.edit_clip_motion(
            clip, self.request.speed, self.request.reverse, self.request.bounce
        )

        return clip

    def _write_gif(self, subclip: VideoFileClip) -> Path:
        """
        Write an edited subclip to disk as a gif.

        Returns:
        -----
            `Path`:
                The path to the extracted gif if the write was successful.

        Raises:
        -----
            `GifWriteError`: If the gif could not be written to disk (from OSError).
        """
        try:
            subclip.write_gif(str(self.request.destpath), logger=None)
        except OSError as e:
            raise GifWriteError(
                f"Error writing gif to {self.request.destpath!r}"
            ) from e
        else:
            return self.request.destpath
