"""Contains Request models that validate and prepare a request for extraction."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import videoxt.preppers as P
import videoxt.validators as V
from videoxt.exceptions import NoAudioError
from videoxt.utils import ToJsonMixin
from videoxt.video import Video


@dataclass
class Request(ABC):
    """
    Protocol defining the interface for validating and preparing extraction requests.

    Public Methods:
    -----
        `validate()` -> `Request`:
            Validate fields if specified and return a validated request of the same
            type.
        `prepare()` -> `PreparedRequest`:
            Construct and return a prepared request using a video and a validated
            request of some type. A prepared request is required by an extractor of the
            same type.

    Properties:
    -----
        `is_validated` (bool): If the request has been validated.
    """

    @abstractmethod
    def validate(self) -> "Request":
        """
        Validate fields if specified and return a validated request of the same type.
        """
        ...

    @abstractmethod
    def prepare(self, video: Video) -> "PreparedRequest":
        """
        Construct and return a prepared request using a video and a validated request
        of some type. A prepared request is required by an extractor of the same type.
        """
        ...

    @property
    @abstractmethod
    def is_validated(self) -> bool:
        """Return True if `Request` has been validated, False otherwise."""
        ...


@dataclass
class BaseRequest(Request):
    """
    Stores, validates and prepares extraction request arguments shared by all methods.

    Fields
    -----
        `start_time` (float | int | str | None):
            Specify the extraction's start time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to 0 if not specified.
        `stop_time` (float | int | str | None):
            Specify the extraction's stop time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to the video duration if not specified.
        `destdir` (Path | None):
            Specify the directory you want to save output to. Defaults to the video's
            directory if not specified.
        `filename` (str | None):
            Specify the name of the extracted file(s). Defaults to the video filename
            if not specified.
        `verbose` (bool | None):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool | None):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.

    Public Methods
    -----
        - `validate()` -> `BaseRequest`:
            Validate fields if specified and return a validated `BaseRequest`.
        - `prepare()` -> `PreparedBaseRequest`:
            Construct and return a prepared base request using a video and a base
            request. A prepared base request is not used by any extractor. Its sole
            purpose is to validate and prepare the shared request arguments.

    Properties
    -----
        - `is_validated` -> `bool`: If the request has been validated.
    """

    start_time: float | int | str | None = None  # XXX: add timedelta support
    stop_time: float | int | str | None = None  # XXX: add timedelta support
    destdir: Path | None = None
    filename: str | None = None
    verbose: bool | None = None
    overwrite: bool | None = None
    fps: float | None = None
    _is_validated: bool = field(init=False)

    def validate(self) -> "BaseRequest":
        """Validate fields if specified and return a validated `BaseRequest`."""
        self._validate_start_time()
        self._validate_stop_time()
        self._validate_fps()
        self._validate_destdir()
        self._validate_filename()
        return self

    def prepare(self, video: Video) -> "PreparedBaseRequest":
        """
        Construct and return a `PreparedBaseRequest` using self and a `Video`.

        Args:
        -----
            `video` (Video): Contains video metadata used to prepare request.

        Returns:
        -----
            `PreparedBaseRequest`: A prepared base extraction request.
        """
        p = PreparedBaseRequest(
            video=video,
            start_time=self.start_time,
            stop_time=self.stop_time,
            fps=self.fps,
            destdir=self.destdir,
            filename=self.filename,
            verbose=self.verbose,
        )
        p.prepare()
        return p

    @property
    def is_validated(self) -> bool:
        """Return True if `Request` has been validated, False otherwise."""
        return self._is_validated

    def _validate_start_time(self) -> float | int | str | None:
        """Validate the requested start time if specified."""
        self.start_time = (
            None if self.start_time is None else V.valid_start_time(self.start_time)
        )
        return self.start_time

    def _validate_stop_time(self) -> float | int | str | None:
        """Validate the requested stop time if specified."""
        self.stop_time = (
            None if self.stop_time is None else V.valid_stop_time(self.stop_time)
        )
        return self.stop_time

    def _validate_fps(self) -> float | None:
        """Validate the requested fps if specified."""
        self.fps = None if self.fps is None else V.positive_float(self.fps)
        return self.fps

    def _validate_destdir(self) -> Path | None:
        """Validate the requested destination directory if specified."""
        self.destdir = None if self.destdir is None else V.valid_dir(self.destdir)
        return self.destdir

    def _validate_filename(self) -> str | None:
        """Validate the requested filename if specified."""
        self.filename = (
            None if self.filename is None else V.valid_filename(self.filename)
        )
        return self.filename


@dataclass
class AudioRequest(BaseRequest):
    """
    Stores, validates and prepares 'audio' extraction request arguments.

    Fields
    -----
        `start_time` (float | int | str | None):
            Specify the extraction's start time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to 0 if not specified.
        `stop_time` (float | int | str | None):
            Specify the extraction's stop time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to the video duration if not specified.
        `destdir` (Path | None):
            Specify the directory you want to save output to. Defaults to the video's
            directory if not specified.
        `filename` (str | None):
            Specify the name of the extracted file(s). Defaults to the video filename
            if not specified.
        `verbose` (bool | None):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool | None):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `audio_format` (str | None):
            Set the extracted audio file format. Defaults to 'mp3' if not specified.
            See: `videoxt.constants.SUPPORTED_AUDIO_FORMATS`.
        `speed` (float | None):
            Set the speed of the extracted audio. A value of 0.5 will halve the speed of
            the extracted audio. Defaults to 1.0 if not specified (no change).
        `bounce` (bool | None):
            If True, bounce the extracted audio bommerang-style. Defaults to False if
            not specified.
        `reverse` (bool | None):
            If True, reverse the extracted audio. Defaults to False if not specified.
        `volume` (float | None):
            Set the volume of the extracted audio. A value of 0.5 will halve the volume
            of the extracted audio. Defaults to 1.0 if not specified (no change).
        `normalize` (bool | None):
            If True, normalize the audio. Normalization adjusts the gain of the audio to
            ensure consistent levels, preventing distortion and enhancing clarity in
            some cases. Defaults to False if not specified.

    Public Methods
    -----
        - `validate()` -> `AudioRequest`:
            Validate fields if specified and return a validated `AudioRequest`.
        - `prepare()` -> `PreparedAudioRequest`:
            Construct and return a prepared audio request using a video and a validated
            `AudioRequest`. A prepared audio request is required by an `AudioExtractor`.

    Properties
    -----
        - `is_validated` -> `bool`: If the request has been validated.
    """

    audio_format: str | None = None
    speed: float | None = None
    bounce: bool | None = None
    reverse: bool | None = None
    volume: float | None = None
    normalize: bool | None = None

    def validate(self) -> "AudioRequest":
        """Validate fields if specified and return a validated `AudioRequest`."""
        super().validate()
        self._validate_audio_format()
        self._validate_speed()
        self._validate_volume()
        self._is_validated = True
        return self

    def prepare(self, video: Video) -> "PreparedAudioRequest":
        """
        Construct and return a `PreparedAudioRequest` using self and a `Video`.

        Fields will validate before preparation if not validated.

        Args:
        -----
            `video` (Video): Contains video metadata used to prepare request.

        Returns:
        -----
            `PreparedAudioRequest`:
                A prepared audio extraction request, required by an `AudioExtractor`.
        """
        if not self.is_validated:
            self.validate()  # XXX: log

        p = PreparedAudioRequest(
            video=video,
            start_time=self.start_time,
            stop_time=self.stop_time,
            destdir=self.destdir,
            filename=self.filename,
            verbose=self.verbose,
            overwrite=self.overwrite,
            fps=self.fps,
            audio_format=self.audio_format,
            speed=self.speed,
            bounce=self.bounce,
            reverse=self.reverse,
            volume=self.volume,
            normalize=self.normalize,
        )
        p.prepare()
        return p

    def _validate_audio_format(self) -> str | None:
        """Validate the requested audio format if specified."""
        self.audio_format = (
            None
            if self.audio_format is None
            else V.valid_audio_format(self.audio_format)
        )
        return self.audio_format

    def _validate_speed(self) -> float | None:
        """Validate the requested speed if specified."""
        self.speed = None if self.speed is None else V.positive_float(self.speed)
        return self.speed

    def _validate_volume(self) -> float | None:
        """Validate the requested volume if specified."""
        self.volume = None if self.volume is None else V.valid_volume(self.volume)
        return self.volume


@dataclass
class ClipRequest(BaseRequest):
    """
    Stores, validates and prepares 'clip' extraction request arguments.

    Recommended usage: Set a short extraction range. The process can be slow for long
    or high-resolution videos.

    Fields
    -----
        `start_time` (float | int | str | None):
            Specify the extraction's start time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to 0 if not specified.
        `stop_time` (float | int | str | None):
            Specify the extraction's stop time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to the video duration if not specified.
        `destdir` (Path | None):
            Specify the directory you want to save output to. Defaults to the video's
            directory if not specified.
        `filename` (str | None):
            Specify the name of the extracted file(s). Defaults to the video filename
            if not specified.
        `verbose` (bool | None):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool | None):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `dimensions` (tuple[int, int] | None):
            Specify the dimensions (frame width, frame height) of the clip. Defaults to
            the video dimensions if not specified.
        `resize` (float | None):
            Resize the dimensions of the clip by a factor of `n`. A value of 0.5
            will halve the dimensions. If you specify `dimensions`, `resize` will apply
            to the dimensions you specify. Defaults to 1.0 if not specified (no change).
        `rotate` (int | None):
            Rotate the clip by `n` degrees. Allowed values: 0, 90, 180 or 270. Defaults
            to 0 if not specified (no change).
        `speed` (float | None):
            Set the speed of the extracted clip. A value of 0.5 will halve the playback
            speed of the clip. Defaults to 1.0 if not specified (no change).
        `bounce` (bool | None):
            If True, bounce the extracted clip bommerang-style. Defaults to False if
            not specified.
        `reverse` (bool | None):
            If True, reverse the extracted clip. Defaults to False if not specified.
        `monochrome` (bool | None):
            If True, apply a black-and-white filter to the clip. Defaults to False if
            not specified.
        `volume` (float | None):
            Set the volume of the extracted clip's audio. A value of 0.5 will halve the
            volume of the clip's audio. Defaults to 1.0 if not specified (no change).
        `normalize` (bool | None):
            If True, normalize the audio. Normalization adjusts the gain of the audio to
            ensure consistent levels, preventing distortion and enhancing clarity in
            some cases. Defaults to False if not specified.

    Public Methods
    -----
        - `validate()` -> `ClipRequest`:
            Validate fields if specified and return a validated `ClipRequest`.
        - `prepare()` -> `PreparedClipRequest`:
            Construct and return a prepared clip request using a video and a validated
            `ClipRequest`. A prepared clip request is required by a `ClipExtractor`.

    Properties
    -----
        - `is_validated` -> `bool`: If the request has been validated.
    """

    dimensions: tuple[int, int] | None = None
    resize: float | None = None
    rotate: int | None = None
    speed: float | None = None
    bounce: bool | None = None
    reverse: bool | None = None
    monochrome: bool | None = None
    volume: float | None = None
    normalize: bool | None = None

    def validate(self) -> "ClipRequest":
        """Validate fields if specified and return a validated `ClipRequest`."""
        super().validate()
        self._validate_resize()
        self._validate_dimensions()
        self._validate_rotate()
        self._validate_speed()
        self._validate_volume()
        self._is_validated = True
        return self

    def prepare(self, video: Video) -> "PreparedClipRequest":
        """
        Construct and return a `PreparedClipRequest` using self and a `Video`.

        Fields will validate before preparation if not validated.

        Args:
        -----
            `video` (Video): Contains video metadata used to prepare request.

        Returns:
        -----
            `PreparedClipRequest`:
                A prepared clip extraction request, required by a `ClipExtractor`.
        """
        if not self.is_validated:
            self.validate()  # XXX: log

        p = PreparedClipRequest(
            video=video,
            start_time=self.start_time,
            stop_time=self.stop_time,
            destdir=self.destdir,
            filename=self.filename,
            verbose=self.verbose,
            overwrite=self.overwrite,
            fps=self.fps,
            dimensions=self.dimensions,
            resize=self.resize,
            rotate=self.rotate,
            speed=self.speed,
            bounce=self.bounce,
            reverse=self.reverse,
            monochrome=self.monochrome,
            volume=self.volume,
            normalize=self.normalize,
        )
        p.prepare()
        return p

    def _validate_resize(self) -> float | None:
        """Validate the requested resize value if specified."""
        self.resize = None if self.resize is None else V.positive_float(self.resize)
        return self.resize

    def _validate_dimensions(self) -> tuple[int, int] | None:
        """Validate the requested dimensions if specified."""
        self.dimensions = (
            None if self.dimensions is None else V.valid_dimensions(self.dimensions)
        )
        return self.dimensions

    def _validate_rotate(self) -> int | None:
        """Validate the requested rotation if specified."""
        self.rotate = None if self.rotate is None else V.valid_rotate_value(self.rotate)
        return self.rotate

    def _validate_speed(self) -> float | None:
        """Validate the requested speed if specified."""
        self.speed = None if self.speed is None else V.positive_float(self.speed)
        return self.speed

    def _validate_volume(self) -> float | None:
        """Validate the requested volume if specified."""
        self.volume = None if self.volume is None else V.valid_volume(self.volume)
        return self.volume


@dataclass
class FramesRequest(BaseRequest):
    """
    Stores, validates and prepares 'frames' extraction request arguments.

    The images are saved to a directory named after the video file, or to a directory
    you specify.

    Fields
    -----
        `start_time` (float | int | str | None):
            Specify the extraction's start time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to 0 if not specified.
        `stop_time` (float | int | str | None):
            Specify the extraction's stop time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to the video duration if not specified.
        `destdir` (Path | None):
            Specify the directory you want to save output to. Defaults to the video's
            directory if not specified.
        `filename` (str | None):
            Specify the name of the extracted file(s). Defaults to the video filename
            if not specified.
        `verbose` (bool | None):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool | None):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `image_format` (str | None):
            Set the extracted image file format. Defaults to 'jpg' if not specified.
            See: `videoxt.constants.SUPPORTED_IMAGE_FORMATS`.
        `capture_rate` (int | None):
            Capture every Nth video frame. Defaults to 1 if not specified, which
            extracts every frame within the extraction range.
        `dimensions` (tuple[int, int] | None):
            Specify the dimensions (frame width, frame height) of the images. Defaults
            to the video dimensions if not specified.
        `resize` (float | None):
            Resize the dimensions of the images by a factor of `n`. A value of 0.5
            will halve the dimensions. If you specify `dimensions`, `resize` will apply
            to the dimensions you specify. Defaults to 1.0 if not specified (no change).
        `rotate` (int | None):
            Rotate the images by `n` degrees. Allowed values: 0, 90, 180 or 270.
            Defaults to 0 if not specified (no change).
        `monochrome` (bool | None):
            If True, apply a black-and-white filter to the images. Defaults to False if
            not specified.

    Public Methods
    -----
        - `validate()` -> `FramesRequest`:
            Validate fields if specified and return a validated `FramesRequest`.
        - `prepare()` -> `PreparedFramesRequest`:
            Construct and return a prepared frames request using a video and a validated
            `FramesRequest`. A prepared frames request is required by a
            `FramesExtractor`.

    Properties
    -----
        - `is_validated` -> `bool`: If the request has been validated.
    """

    image_format: str | None = None
    capture_rate: int | None = None
    dimensions: tuple[int, int] | None = None
    resize: float | None = None
    rotate: int | None = None
    monochrome: bool | None = None

    def validate(self) -> "FramesRequest":
        """Validate fields if specified and return a validated `FramesRequest`."""
        super().validate()
        self._validate_image_format()
        self._validate_capture_rate()
        self._validate_resize()
        self._validate_dimensions()
        self._validate_rotate()
        self._is_validated = True
        return self

    def prepare(self, video: Video) -> "PreparedFramesRequest":
        """
        Construct and return a `PreparedFramesRequest` using self and a `Video`.

        Fields will validate before preparation if not validated.

        Args:
        -----
            `video` (Video): Contains video metadata used to prepare request.

        Returns:
        -----
            `PreparedFramesRequest`:
                A prepared frames extraction request, required by a `FramesExtractor`.
        """
        if not self.is_validated:
            self.validate()  # XXX: log

        p = PreparedFramesRequest(
            video=video,
            start_time=self.start_time,
            stop_time=self.stop_time,
            destdir=self.destdir,
            filename=self.filename,
            verbose=self.verbose,
            overwrite=self.overwrite,
            fps=self.fps,
            image_format=self.image_format,
            capture_rate=self.capture_rate,
            dimensions=self.dimensions,
            resize=self.resize,
            rotate=self.rotate,
            monochrome=self.monochrome,
        )
        p.prepare()
        return p

    def _validate_image_format(self) -> str | None:
        """Validate the requested image format if specified."""
        self.image_format = (
            None
            if self.image_format is None
            else V.valid_image_format(self.image_format)
        )
        return self.image_format

    def _validate_capture_rate(self) -> int | None:
        """Validate the requested capture rate if specified."""
        self.capture_rate = (
            None if self.capture_rate is None else V.positive_int(self.capture_rate)
        )

        return self.capture_rate

    def _validate_resize(self) -> float | None:
        """Validate the requested resize value if specified."""
        self.resize = None if self.resize is None else V.positive_float(self.resize)
        return self.resize

    def _validate_dimensions(self) -> tuple[int, int] | None:
        """Validate the requested dimensions if specified."""
        self.dimensions = (
            None if self.dimensions is None else V.valid_dimensions(self.dimensions)
        )
        return self.dimensions

    def _validate_rotate(self) -> int | None:
        """Validate the requested rotation if specified."""
        self.rotate = None if self.rotate is None else V.valid_rotate_value(self.rotate)
        return self.rotate


@dataclass
class GifRequest(BaseRequest):
    """
    Stores, validates and prepares 'gif' extraction request arguments.

    Recommended usage: Set a short extraction range. The process can be slow for long
    or high-resolution videos.

    Fields
    -----
        `start_time` (float | int | str | None):
            Specify the extraction's start time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to 0 if not specified.
        `stop_time` (float | int | str | None):
            Specify the extraction's stop time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to the video duration if not specified.
        `destdir` (Path | None):
            Specify the directory you want to save output to. Defaults to the video's
            directory if not specified.
        `filename` (str | None):
            Specify the name of the extracted file(s). Defaults to the video filename
            if not specified.
        `verbose` (bool | None):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool | None):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `dimensions` (tuple[int, int] | None):
            Specify the dimensions (frame width, frame height) of the gif. Defaults to
            the video dimensions if not specified.
        `resize` (float | None):
            Resize the dimensions of the gif by a factor of `n`. A value of 0.5
            will halve the dimensions. If you specify `dimensions`, `resize` will apply
            to the dimensions you specify. Defaults to 1.0 if not specified (no change).
        `rotate` (int | None):
            Rotate the gif by `n` degrees. Allowed values: 0, 90, 180 or 270. Defaults
            to 0 if not specified (no change).
        `speed` (float | None):
            Set the speed of the extracted gif. A value of 0.5 will halve the playback
            speed of the gif. Defaults to 1.0 if not specified (no change).
        `bounce` (bool | None):
            If True, bounce the extracted gif bommerang-style. Defaults to False if
            not specified.
        `reverse` (bool | None):
            If True, reverse the extracted gif. Defaults to False if not specified.
        `monochrome` (bool | None):
            If True, apply a black-and-white filter to the gif. Defaults to False if
            not specified.

    Public Methods
    -----
        - `validate()` -> `GifRequest`:
            Validate fields if specified and return a validated `GifRequest`.
        - `prepare()` -> `PreparedGifRequest`:
            Construct and return a prepared gif request using a video and a validated
            `GifRequest`. A prepared gif request is required by a `GifExtractor`.

    Properties
    -----
        - `is_validated` -> `bool`: If the request has been validated.
    """

    dimensions: tuple[int, int] | None = None
    resize: float | None = None
    rotate: int | None = None
    speed: float | None = None
    bounce: bool | None = None
    reverse: bool | None = None
    monochrome: bool | None = None

    def validate(self) -> "GifRequest":
        """Validate fields if specified and return a validated `GifRequest`."""
        super().validate()
        self._validate_resize()
        self._validate_dimensions()
        self._validate_rotate()
        self._validate_speed()
        self._is_validated = True
        return self

    def prepare(self, video: Video) -> "PreparedGifRequest":
        """
        Construct and return a `PreparedGifRequest` using self and a `Video`.

        Fields will validate before preparation if not validated.

        Args:
        -----
            `video` (Video): Contains video metadata used to prepare request.

        Returns:
        -----
            `PreparedGifRequest`:
                A prepared gif extraction request, required by a `GifExtractor`.
        """
        if not self.is_validated:
            self.validate()  # XXX: log

        p = PreparedGifRequest(
            video=video,
            start_time=self.start_time,
            stop_time=self.stop_time,
            destdir=self.destdir,
            filename=self.filename,
            verbose=self.verbose,
            overwrite=self.overwrite,
            fps=self.fps,
            dimensions=self.dimensions,
            resize=self.resize,
            rotate=self.rotate,
            speed=self.speed,
            bounce=self.bounce,
            reverse=self.reverse,
            monochrome=self.monochrome,
        )
        p.prepare()
        return p

    def _validate_resize(self) -> float | None:
        """Validate the requested resize value if specified."""
        self.resize = None if self.resize is None else V.positive_float(self.resize)
        return self.resize

    def _validate_dimensions(self) -> tuple[int, int] | None:
        """Validate the requested dimensions if specified."""
        self.dimensions = (
            None if self.dimensions is None else V.valid_dimensions(self.dimensions)
        )
        return self.dimensions

    def _validate_rotate(self) -> int | None:
        """Validate the requested rotation if specified."""
        self.rotate = None if self.rotate is None else V.valid_rotate_value(self.rotate)
        return self.rotate

    def _validate_speed(self) -> float | None:
        """Validate the requested speed if specified."""
        self.speed = None if self.speed is None else V.positive_float(self.speed)
        return self.speed


@dataclass
class PreparedRequest(ABC, ToJsonMixin):
    """
    Protocol defining the interface for preparing requests for extraction.

    Public Methods:
    -----
        - `prepare()` -> `PreparedRequest`:
            Prepare fields and return a fully prepared request of some type.
        - `json()` -> `str`:
            Return a JSON string representation of the prepared request type.
        - `verbose_print()` -> `None`:
            Print the JSON string to console with a title, without private keys.

    Properties:
    -----
        - `is_prepared` -> `bool`: If the request has been prepared.
        - `is_verbose` -> `bool | None`: Return the state of the verbose field.
    """

    @abstractmethod
    def prepare(self) -> "PreparedRequest":
        """Prepare fields and return a fully prepared request of some type."""
        ...

    @property
    @abstractmethod
    def is_prepared(self) -> bool:
        """Return True if the request has been prepared, False otherwise."""
        ...

    @property
    @abstractmethod
    def is_verbose(self) -> bool | None:
        """Return the state of the verbose field."""
        ...


@dataclass
class PreparedBaseRequest(PreparedRequest):
    """
    Prepares and stores request arguments shared by all extraction methods.

    Fields
    -----
        `video` (Video):
            The object containing video metadata used to prepare the request.
        `start_time` (float | int | str | None):
            Specify the extraction's start time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to 0 if not specified.
        `stop_time` (float | int | str | None):
            Specify the extraction's stop time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to the video duration if not specified.
        `destdir` (Path | None):
            Specify the directory you want to save output to. Defaults to the video's
            directory if not specified.
        `filename` (str | None):
            Specify the name of the extracted file(s). Defaults to the video filename
            if not specified.
        `verbose` (bool | None):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool | None):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `destpath` (Path):
            The destination path of the extracted file or directory. Not initialized.
        `extraction_range` (dict):
            The range represented as seconds, as timestamps, and frame numbers.
            Not initialized.

    Public Methods
    -----
        - `prepare()` -> `PreparedBaseRequest`:
            Prepare fields and return a fully prepared base request.
        - `json()` -> `str`:
            Return a JSON string representation of the prepared base request.
        - `verbose_print()` -> `None`:
            Print the JSON string to console with a title, without private keys.

    Properties:
    -----
        - `is_prepared` -> `bool`: If the request has been prepared.
        - `is_verbose` -> `bool | None`: Return the state of the verbose field.
    """

    video: Video
    start_time: float | int | str | None = None
    stop_time: float | int | str | None = None
    destdir: Path | None = None
    filename: str | None = None
    verbose: bool | None = None
    overwrite: bool | None = None
    fps: float | None = None
    destpath: Path = field(init=False)
    extraction_range: dict[str, Any] = field(init=False, default_factory=dict)
    _is_prepared: bool = field(init=False)

    def prepare(self) -> "PreparedBaseRequest":
        """Prepare fields and return a `PreparedBaseRequest`."""
        self._prepare_start_time()
        self._prepare_stop_time()
        self._prepare_fps()
        self._prepare_extraction_range()
        self._prepare_verbose()
        self._prepare_overwrite()
        return self

    @property
    def is_prepared(self) -> bool:
        """Return True if the request has been prepared, False otherwise."""
        return self._is_prepared

    @property
    def is_verbose(self) -> bool | None:
        """Return the state of the verbose field."""
        return self.verbose

    def _prepare_start_time(self) -> float | int | str:
        """Set start time to 0 if not specified."""
        self.start_time = P.prepare_start_time(self.start_time)
        return self.start_time

    def _prepare_stop_time(self) -> float | int | str:
        """Set stop time to video duration if not specified."""
        self.stop_time = P.prepare_stop_time(
            self.video.duration_seconds, self.stop_time
        )
        return self.stop_time

    def _prepare_fps(self) -> float:
        """Set fps to video fps if not specified."""
        self.fps = P.prepare_fps(self.video.fps, self.fps)
        return self.fps

    def _prepare_extraction_range(self) -> dict[str, Any]:
        """Prepare, set and return a dictionary representing the extraction range."""
        self.extraction_range = P.prepare_extraction_range(
            self.video.duration_seconds,
            self.video.frame_count,
            self.start_time,
            self.stop_time,
            self.fps,
        )

        return self.extraction_range

    def _prepare_verbose(self) -> bool:
        """Set verbose to False if not specified."""
        if self.verbose is None:
            self.verbose = False
        return self.verbose

    def _prepare_overwrite(self) -> bool:
        """Set overwrite to False if not specified."""
        if self.overwrite is None:
            self.overwrite = False
        return self.overwrite


@dataclass
class PreparedAudioRequest(PreparedBaseRequest):
    """
    Prepares and stores 'audio' extraction request arguments.

    Fields
    -----
        `video` (Video):
            The object containing video metadata used to prepare the request.
        `start_time` (float | int | str | None):
            Specify the extraction's start time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to 0 if not specified.
        `stop_time` (float | int | str | None):
            Specify the extraction's stop time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to the video duration if not specified.
        `destdir` (Path | None):
            Specify the directory you want to save output to. Defaults to the video's
            directory if not specified.
        `filename` (str | None):
            Specify the name of the extracted file(s). Defaults to the video filename
            if not specified.
        `verbose` (bool | None):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool | None):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `destpath` (Path):
            The destination path of the extracted file or directory. Not initialized.
        `extraction_range` (dict):
            The range represented as seconds, as timestamps, and frame numbers.
            Not initialized.
        `audio_format` (str | None):
            Set the extracted audio file format. Defaults to 'mp3' if not specified.
            See: `videoxt.constants.SUPPORTED_AUDIO_FORMATS`.
        `speed` (float | None):
            Set the speed of the extracted audio. A value of 0.5 will halve the speed of
            the extracted audio. Defaults to 1.0 if not specified (no change).
        `bounce` (bool | None):
            If True, bounce the extracted audio bommerang-style. Defaults to False if
            not specified.
        `reverse` (bool | None):
            If True, reverse the extracted audio. Defaults to False if not specified.
        `volume` (float | None):
            Set the volume of the extracted audio. A value of 0.5 will halve the volume
            of the extracted audio. Defaults to 1.0 if not specified (no change).
        `normalize` (bool | None):
            If True, normalize the audio. Normalization adjusts the gain of the audio to
            ensure consistent levels, preventing distortion and enhancing clarity in
            some cases. Defaults to False if not specified.

    Public Methods
    -----
        - `prepare()` -> `PreparedAudioRequest`:
            Prepare fields and return a fully prepared audio request, required by an
            `AudioExtractor`.
        - `json()` -> `str`:
            Return a JSON string representation of the prepared audio request.
        - `verbose_print()` -> `None`:
            Print the JSON string to console with a title, without private keys.

    Properties:
    -----
        - `is_prepared` -> `bool`: If the request has been prepared.
        - `is_verbose` -> `bool | None`: Return the state of the verbose field.
    """

    audio_format: str | None = None
    speed: float | None = None
    bounce: bool | None = None
    reverse: bool | None = None
    volume: float | None = None
    normalize: bool | None = None

    def prepare(self) -> "PreparedAudioRequest":
        """
        Prepare request fields and return a `PreparedAudioRequest`, required by an
        `AudioExtractor`.
        """
        self._check_video_has_audio()
        super().prepare()
        self._prepare_audio_format()
        self._prepare_destpath()
        self._prepare_speed()
        self._prepare_bounce()
        self._prepare_reverse()
        self._prepare_volume()
        self._prepare_normalize()
        self._is_prepared = True
        return self

    def _check_video_has_audio(self) -> None:
        """Raise `NoAudioError` if the video does not have audio."""
        if not self.video.has_audio:
            raise NoAudioError("Video does not have audio.")

    def _prepare_audio_format(self) -> str:
        """Set audio format to 'mp3' if not specified."""
        if self.audio_format is None:
            self.audio_format = "mp3"
        return self.audio_format

    def _prepare_destpath(self) -> Path:
        """Set the destination path the extracted audio file will be saved to."""
        self.destpath = P.prepare_destpath(
            self.video.filepath,
            self.filename,
            self.destdir,
            self.audio_format,
            self.overwrite,
        )

        return self.destpath

    def _prepare_speed(self) -> float:
        """Set speed to 1.0 if not specified."""
        if self.speed is None:
            self.speed = 1.0
        return self.speed

    def _prepare_bounce(self) -> bool:
        """Set bounce to False if not specified."""
        if self.bounce is None:
            self.bounce = False
        return self.bounce

    def _prepare_reverse(self) -> bool:
        """Set reverse to False if not specified."""
        if self.reverse is None:
            self.reverse = False
        return self.reverse

    def _prepare_volume(self) -> float:
        """Set volume to 1.0 if not specified."""
        if self.volume is None:
            self.volume = 1.0
        return self.volume

    def _prepare_normalize(self) -> bool:
        """Set normalize to False if not specified."""
        if self.normalize is None:
            self.normalize = False
        return self.normalize


@dataclass
class PreparedClipRequest(PreparedBaseRequest):
    """
    Prepares and stores 'clip' extraction request arguments.

    Fields
    -----
        `video` (Video):
            The object containing video metadata used to prepare the request.
        `start_time` (float | int | str | None):
            Specify the extraction's start time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to 0 if not specified.
        `stop_time` (float | int | str | None):
            Specify the extraction's stop time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to the video duration if not specified.
        `destdir` (Path | None):
            Specify the directory you want to save output to. Defaults to the video's
            directory if not specified.
        `filename` (str | None):
            Specify the name of the extracted file(s). Defaults to the video filename
            if not specified.
        `verbose` (bool | None):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool | None):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `destpath` (Path):
            The destination path of the extracted file or directory. Not initialized.
        `extraction_range` (dict):
            The range represented as seconds, as timestamps, and frame numbers.
            Not initialized.
        `dimensions` (tuple[int, int] | None):
            Specify the dimensions (frame width, frame height) of the clip. Defaults to
            the video dimensions if not specified.
        `resize` (float | None):
            Resize the dimensions of the clip by a factor of `n`. A value of 0.5
            will halve the dimensions. If you specify `dimensions`, `resize` will apply
            to the dimensions you specify. Defaults to 1.0 if not specified (no change).
        `rotate` (int | None):
            Rotate the clip by `n` degrees. Allowed values: 0, 90, 180 or 270. Defaults
            to 0 if not specified (no change).
        `speed` (float | None):
            Set the speed of the extracted clip. A value of 0.5 will halve the playback
            speed of the clip. Defaults to 1.0 if not specified (no change).
        `bounce` (bool | None):
            If True, bounce the extracted clip bommerang-style. Defaults to False if
            not specified.
        `reverse` (bool | None):
            If True, reverse the extracted clip. Defaults to False if not specified.
        `monochrome` (bool | None):
            If True, apply a black-and-white filter to the clip. Defaults to False if
            not specified.
        `volume` (float | None):
            Set the volume of the extracted clip's audio. A value of 0.5 will halve the
            volume of the clip's audio. Defaults to 1.0 if not specified (no change).
        `normalize` (bool | None):
            If True, normalize the audio. Normalization adjusts the gain of the audio to
            ensure consistent levels, preventing distortion and enhancing clarity in
            some cases. Defaults to False if not specified.

    Public Methods
    -----
        - `prepare()` -> `PreparedClipRequest`:
            Prepare fields and return a fully prepared clip request, required by a
            `ClipExtractor`.
        - `json()` -> `str`:
            Return a JSON string representation of the prepared clip request.
        - `verbose_print()` -> `None`:
            Print the JSON string to console with a title, without private keys.

    Properties:
    -----
        - `is_prepared` -> `bool`: If the request has been prepared.
        - `is_verbose` -> `bool | None`: Return the state of the verbose field.
    """

    dimensions: tuple[int, int] | None = None
    resize: float | None = None
    rotate: int | None = None
    speed: float | None = None
    bounce: bool | None = None
    reverse: bool | None = None
    monochrome: bool | None = None
    volume: float | None = None
    normalize: bool | None = None

    def prepare(self) -> "PreparedClipRequest":
        """
        Prepare request fields and return a `PreparedClipRequest`, required by a
        `ClipExtractor`.
        """
        super().prepare()
        self._prepare_destpath()
        self._prepare_resize()
        self._prepare_dimensions()
        self._prepare_rotate()
        self._prepare_speed()
        self._prepare_bounce()
        self._prepare_reverse()
        self._prepare_monochrome()
        self._prepare_volume()
        self._prepare_normalize()
        self._is_prepared = True
        return self

    def _prepare_destpath(self) -> Path:
        """Set the destination path the extracted clip will be saved to."""
        self.destpath = P.prepare_destpath(
            self.video.filepath,
            self.filename,
            self.destdir,
            ".mp4",
            self.overwrite,
        )

        return self.destpath

    def _prepare_resize(self) -> float:
        """Set resize to 1.0 if not specified."""
        if self.resize is None:
            self.resize = 1.0
        return self.resize

    def _prepare_dimensions(self) -> tuple[int, int]:
        """Set dimensions to the video dimensions if not specified."""
        self.dimensions = P.prepare_dimensions(
            self.video.dimensions, self.dimensions, self.resize
        )
        return self.dimensions

    def _prepare_rotate(self) -> int:
        """Set rotate to 0 if not specified."""
        if self.rotate is None:
            self.rotate = 0
        return self.rotate

    def _prepare_speed(self) -> float:
        """Set speed to 1.0 if not specified."""
        if self.speed is None:
            self.speed = 1.0
        return self.speed

    def _prepare_bounce(self) -> bool:
        """Set bounce to False if not specified."""
        if self.bounce is None:
            self.bounce = False
        return self.bounce

    def _prepare_reverse(self) -> bool:
        """Set reverse to False if not specified."""
        if self.reverse is None:
            self.reverse = False
        return self.reverse

    def _prepare_monochrome(self) -> bool:
        """Set monochrome to False if not specified."""
        if self.monochrome is None:
            self.monochrome = False
        return self.monochrome

    def _prepare_volume(self) -> float:
        """Set volume to 1.0 if not specified."""
        if self.volume is None:
            self.volume = 1.0
        return self.volume

    def _prepare_normalize(self) -> bool:
        """Set normalize to False if not specified."""
        if self.normalize is None:
            self.normalize = False
        return self.normalize


@dataclass
class PreparedFramesRequest(PreparedBaseRequest):
    """
    Prepares and stores 'frames' extraction request arguments.

    Fields
    -----
        `video` (Video):
            The object containing video metadata used to prepare the request.
        `start_time` (float | int | str | None):
            Specify the extraction's start time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to 0 if not specified.
        `stop_time` (float | int | str | None):
            Specify the extraction's stop time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to the video duration if not specified.
        `destdir` (Path | None):
            Specify the directory you want to save output to. Defaults to the video's
            directory if not specified.
        `filename` (str | None):
            Specify the name of the extracted file(s). Defaults to the video filename
            if not specified.
        `verbose` (bool | None):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool | None):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `image_format` (str | None):
            Set the extracted image file format. Defaults to 'jpg' if not specified.
            See: `videoxt.constants.SUPPORTED_IMAGE_FORMATS`.
        `capture_rate` (int | None):
            Capture every Nth video frame. Defaults to 1 if not specified, which
            extracts every frame within the extraction range.
        `dimensions` (tuple[int, int] | None):
            Specify the dimensions (frame width, frame height) of the images. Defaults
            to the video dimensions if not specified.
        `resize` (float | None):
            Resize the dimensions of the images by a factor of `n`. A value of 0.5
            will halve the dimensions. If you specify `dimensions`, `resize` will apply
            to the dimensions you specify. Defaults to 1.0 if not specified (no change).
        `rotate` (int | None):
            Rotate the images by `n` degrees. Allowed values: 0, 90, 180 or 270.
            Defaults to 0 if not specified (no change).
        `monochrome` (bool | None):
            If True, apply a black-and-white filter to the images. Defaults to False if
            not specified.
        `images_expected` (int):
            The number of images expected to be written to disk. Not initialized.

    Public Methods
    -----
        - `prepare()` -> `PreparedFramesRequest`:
            Prepare fields and return a fully prepared frames request, required by a
            `FramesExtractor`.
        - `json()` -> `str`:
            Return a JSON string representation of the prepared frames request.
        - `verbose_print()` -> `None`:
            Print the JSON string to console with a title, without private keys.

    Properties:
    -----
        - `is_prepared` -> `bool`: If the request has been prepared.
        - `is_verbose` -> `bool | None`: Return the state of the verbose field.
    """

    image_format: str | None = None
    capture_rate: int | None = None
    dimensions: tuple[int, int] | None = None
    resize: float | None = None
    rotate: int | None = None
    monochrome: bool | None = None
    images_expected: int = field(init=False)

    def prepare(self) -> "PreparedFramesRequest":
        """
        Prepare request fields and return a `PreparedFramesRequest`, required by a
        `FramesExtractor`.
        """
        super().prepare()
        self._prepare_destpath()
        self._prepare_filename()
        self._prepare_image_format()
        self._prepare_capture_rate()
        self._prepare_resize()
        self._prepare_dimensions()
        self._prepare_rotate()
        self._prepare_monochrome()
        self._prepare_images_expected()
        self._is_prepared = True
        return self

    def _prepare_destpath(self) -> Path:
        """Set the directory the extracted images will be saved to."""
        self.destpath = P.prepare_destpath_frames(
            self.video.filepath, self.destdir, self.overwrite
        )
        return self.destpath

    def _prepare_filename(self) -> str:
        """Set filename to the video filename. Used for naming the extracted images."""
        if self.filename is None:
            self.filename = self.video.filepath.stem
        return self.filename

    def _prepare_image_format(self) -> str:
        """Set image format to 'jpg' if not specified."""
        if self.image_format is None:
            self.image_format = "jpg"
        return self.image_format

    def _prepare_capture_rate(self) -> int:
        """Set capture rate to 1 if not specified."""
        if self.capture_rate is None:
            self.capture_rate = 1
        return self.capture_rate

    def _prepare_resize(self) -> float:
        """Set resize to 1.0 if not specified."""
        if self.resize is None:
            self.resize = 1.0
        return self.resize

    def _prepare_dimensions(self) -> tuple[int, int]:
        """Set dimensions to the video dimensions if not specified."""
        self.dimensions = P.prepare_dimensions(
            self.video.dimensions, self.dimensions, self.resize
        )
        return self.dimensions

    def _prepare_rotate(self) -> int:
        """Set rotate to 0 if not specified."""
        if self.rotate is None:
            self.rotate = 0
        return self.rotate

    def _prepare_monochrome(self) -> bool:
        """Set monochrome to False if not specified."""
        if self.monochrome is None:
            self.monochrome = False
        return self.monochrome

    def _prepare_images_expected(self) -> int:
        """Set the number of images (frames) expected to be written to disk."""
        self.images_expected = P.prepare_images_expected(
            self.extraction_range.get("start_frame", None),
            self.extraction_range.get("stop_frame", None),
            self.capture_rate,
        )

        return self.images_expected


@dataclass
class PreparedGifRequest(PreparedBaseRequest):
    """
    Prepares and stores 'gif' extraction request arguments.

    Fields
    -----
        `video` (Video):
            The object containing video metadata used to prepare the request.
        `start_time` (float | int | str | None):
            Specify the extraction's start time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to 0 if not specified.
        `stop_time` (float | int | str | None):
            Specify the extraction's stop time in seconds, or as a string in "HH:MM:SS"
            format. Defaults to the video duration if not specified.
        `destdir` (Path | None):
            Specify the directory you want to save output to. Defaults to the video's
            directory if not specified.
        `filename` (str | None):
            Specify the name of the extracted file(s). Defaults to the video filename
            if not specified.
        `verbose` (bool | None):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool | None):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `dimensions` (tuple[int, int] | None):
            Specify the dimensions (frame width, frame height) of the gif. Defaults to
            the video dimensions if not specified.
        `resize` (float | None):
            Resize the dimensions of the gif by a factor of `n`. A value of 0.5
            will halve the dimensions. If you specify `dimensions`, `resize` will apply
            to the dimensions you specify. Defaults to 1.0 if not specified (no change).
        `rotate` (int | None):
            Rotate the gif by `n` degrees. Allowed values: 0, 90, 180 or 270. Defaults
            to 0 if not specified (no change).
        `speed` (float | None):
            Set the speed of the extracted gif. A value of 0.5 will halve the playback
            speed of the gif. Defaults to 1.0 if not specified (no change).
        `bounce` (bool | None):
            If True, bounce the extracted gif bommerang-style. Defaults to False if
            not specified.
        `reverse` (bool | None):
            If True, reverse the extracted gif. Defaults to False if not specified.
        `monochrome` (bool | None):
            If True, apply a black-and-white filter to the gif. Defaults to False if
            not specified.

    Public Methods
    -----
        - `prepare()` -> `PreparedGifRequest`:
            Prepare fields and return a fully prepared gif request, required by a
            `GifExtractor`.
        - `json()` -> `str`:
            Return a JSON string representation of the prepared gif request.
        - `verbose_print()` -> `None`:
            Print the JSON string to console with a title, without private keys.

    Properties:
    -----
        - `is_prepared` -> `bool`: If the request has been prepared.
        - `is_verbose` -> `bool | None`: Return the state of the verbose field.
    """

    dimensions: tuple[int, int] | None = None
    resize: float | None = None
    rotate: int | None = None
    speed: float | None = None
    bounce: bool | None = None
    reverse: bool | None = None
    monochrome: bool | None = None

    def prepare(self) -> "PreparedGifRequest":
        """
        Prepare request fields and return a `PreparedGifRequest`, required by a
        `GifExtractor`.
        """
        super().prepare()
        self._prepare_destpath()
        self._prepare_resize()
        self._prepare_dimensions()
        self._prepare_rotate()
        self._prepare_speed()
        self._prepare_bounce()
        self._prepare_monochrome()
        self._prepare_reverse()
        self._is_prepared = True
        return self

    def _prepare_destpath(self) -> Path:
        """Set the destination path the extracted clip will be saved to."""
        self.destpath = P.prepare_destpath(
            self.video.filepath,
            self.filename,
            self.destdir,
            ".gif",
            self.overwrite,
        )

        return self.destpath

    def _prepare_resize(self) -> float:
        """Set resize to 1.0 if not specified."""
        if self.resize is None:
            self.resize = 1.0
        return self.resize

    def _prepare_dimensions(self) -> tuple[int, int]:
        """Set dimensions to the video dimensions if not specified."""
        self.dimensions = P.prepare_dimensions(
            self.video.dimensions, self.dimensions, self.resize
        )
        return self.dimensions

    def _prepare_rotate(self) -> int:
        """Set rotate to 0 if not specified."""
        if self.rotate is None:
            self.rotate = 0
        return self.rotate

    def _prepare_speed(self) -> float:
        """Set speed to 1.0 if not specified."""
        if self.speed is None:
            self.speed = 1.0
        return self.speed

    def _prepare_bounce(self) -> bool:
        """Set bounce to False if not specified."""
        if self.bounce is None:
            self.bounce = False
        return self.bounce

    def _prepare_monochrome(self) -> bool:
        """Set monochrome to False if not specified."""
        if self.monochrome is None:
            self.monochrome = False
        return self.monochrome

    def _prepare_reverse(self) -> bool:
        """Set reverse to False if not specified."""
        if self.reverse is None:
            self.reverse = False
        return self.reverse
