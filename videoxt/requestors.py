"""Request objects that validate and prepare extraction requests for Extrator objects."""
import typing as t
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

import videoxt.preppers as P
import videoxt.validators as V
from videoxt.video import Video


@dataclass
class Request(ABC):
    """Abstract class for all requests. All requests adhere to this interface."""

    video: Video

    @abstractmethod
    def __post_init__(self) -> None:
        """Validate user input."""
        pass

    @abstractmethod
    def prepare_request(self) -> None:
        """Prepare request for extraction."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Human-readable representation of the request.

        Prints to console prior to extraction if `verbose` is `True`."""
        pass


@dataclass
class BaseRequest(Request):
    """Base request class for all requests. All requests inherit from this class."""

    video: Video
    start_time: t.Union[float, str] = "0:00:00"
    stop_time: t.Optional[t.Union[float, str]] = None
    fps: t.Optional[float] = None
    destdir: t.Optional[Path] = None
    filename: t.Optional[str] = None
    verbose: bool = False
    time_range: P.TimeRange = field(init=False)

    def __post_init__(self) -> None:
        """Validate `BaseRequest` attributes."""
        self.start_time = V.valid_start_time(self.start_time)

        if self.stop_time is not None:
            self.stop_time = V.valid_stop_time(self.stop_time)

        if self.fps is not None:
            self.fps = V.positive_float(self.fps)

        if self.destdir is not None:
            self.destdir = V.valid_dir(self.destdir)

        if self.filename is not None:
            self.filename = V.valid_filename(self.filename)

    def prepare_request(self) -> None:
        """Prepare `BaseRequest` attributes."""
        self.fps = P.prepare_fps(self.video.properties.fps, self.fps)
        self.time_range = P.prepare_time_range(
            self.start_time,
            self.stop_time,
            self.video.properties.length_timestamp,
            self.video.properties.length_seconds,
            self.video.properties.frame_count,
            self.fps,
        )

        V.valid_extraction_range(
            self.time_range.start_second,
            self.time_range.stop_second,
            self.video.properties.length_seconds,
        )

    def __str__(self) -> str:
        import videoxt.displays

        return videoxt.displays.base_request_str(self)


@dataclass
class AudioRequest(BaseRequest):
    """Request object for audio extraction."""

    audio_format: str = "mp3"
    speed: float = 1.0
    volume: float = 1.0
    bounce: bool = False
    reverse: bool = False
    normalize: bool = False
    filepath: Path = field(init=False)

    def __post_init__(self) -> None:
        """Validate `AudioRequest` attributes, call `prepare_request` method."""
        super().__post_init__()

        self.audio_format = V.valid_audio_format(self.audio_format)
        self.speed = V.positive_float(self.speed)
        self.volume = V.non_negative_float(self.volume)

        self.prepare_request()

    def prepare_request(self) -> None:
        """Prepare `AudioRequest` attributes."""
        super().prepare_request()

        self.destdir = P.prepare_destdir(self.video.filepath.parent, self.destdir)
        self.filepath = P.prepare_filepath(
            self.video.filepath.stem,
            self.filename,
            self.destdir,
            self.audio_format,
        )

    def __str__(self) -> str:
        import videoxt.displays

        return super().__str__() + videoxt.displays.audio_request_str(self)


@dataclass
class ClipRequest(BaseRequest):
    """Request object for clip extraction."""

    resize: float = 1.0
    rotate: int = 0
    speed: float = 1.0
    volume: float = 1.0
    monochrome: bool = False
    bounce: bool = False
    reverse: bool = False
    normalize: bool = False
    dimensions: t.Optional[t.Tuple[int, int]] = None
    filepath: Path = field(init=False)

    def __post_init__(self) -> None:
        """Validate `ClipRequest` attributes, call `prepare_request` method."""
        super().__post_init__()

        self.resize = V.valid_resize_value(self.resize)
        self.rotate = V.valid_rotate_value(self.rotate)
        self.speed = V.positive_float(self.speed)
        self.volume = V.non_negative_float(self.volume)

        if self.dimensions is not None:
            self.dimensions = V.valid_dimensions(self.dimensions)

        self.prepare_request()

    def prepare_request(self) -> None:
        """Prepare `ClipRequest` attributes."""
        super().prepare_request()

        self.destdir = P.prepare_destdir(self.video.filepath.parent, self.destdir)
        self.dimensions = P.prepare_dimensions(
            self.video.properties.dimensions, self.dimensions, self.resize
        )
        self.filepath = P.prepare_filepath(
            self.video.filepath.stem, self.filename, self.destdir, "mp4"
        )

    def __str__(self) -> str:
        import videoxt.displays

        return super().__str__() + videoxt.displays.clip_request_str(self)


@dataclass
class FramesRequest(BaseRequest):
    """Request object for frames extraction."""

    image_format: str = "jpg"
    capture_rate: int = 1
    resize: float = 1.0
    rotate: int = 0
    monochrome: bool = False
    dimensions: t.Optional[t.Tuple[int, int]] = None
    images_expected: int = field(init=False)

    def __post_init__(self) -> None:
        """Validate `FramesRequest` attributes, call `prepare_request` method."""
        super().__post_init__()

        self.image_format = V.valid_image_format(self.image_format)
        self.capture_rate = V.positive_int(self.capture_rate)
        self.resize = V.valid_resize_value(self.resize)
        self.rotate = V.valid_rotate_value(self.rotate)

        if self.dimensions is not None:
            self.dimensions = V.valid_dimensions(self.dimensions)

        self.prepare_request()

    def prepare_request(self) -> None:
        """Prepare `FramesRequest` attributes."""
        super().prepare_request()

        self.capture_rate = V.valid_capture_rate(
            self.capture_rate, self.time_range.start_frame, self.time_range.stop_frame
        )
        self.images_expected = P.prepare_images_expected(
            self.time_range.start_frame, self.time_range.stop_frame, self.capture_rate
        )
        self.destdir = P.prepare_destdir_frames(
            self.video.filepath.parent, self.video.filepath.name, self.destdir
        )
        self.filename = P.prepare_filename_frames(
            self.video.filepath.stem, self.filename
        )
        self.dimensions = P.prepare_dimensions(
            self.video.properties.dimensions, self.dimensions, self.resize
        )

    def __str__(self) -> str:
        import videoxt.displays

        return super().__str__() + videoxt.displays.frames_request_str(self)


@dataclass
class GifRequest(BaseRequest):
    """Request object for gif extraction."""

    resize: float = 1.0
    rotate: int = 0
    speed: float = 1.0
    monochrome: bool = False
    bounce: bool = False
    reverse: bool = False
    dimensions: t.Optional[t.Tuple[int, int]] = None
    filepath: Path = field(init=False)

    def __post_init__(self) -> None:
        """Validate `GifRequest` attributes, call `prepare_request` method."""
        super().__post_init__()

        self.resize = V.valid_resize_value(self.resize)
        self.rotate = V.valid_rotate_value(self.rotate)
        self.speed = V.positive_float(self.speed)

        if self.dimensions is not None:
            self.dimensions = V.valid_dimensions(self.dimensions)

        self.prepare_request()

    def prepare_request(self) -> None:
        """Prepare `GifRequest` attributes."""
        super().prepare_request()

        self.destdir = P.prepare_destdir(self.video.filepath.parent, self.destdir)
        self.dimensions = P.prepare_dimensions(
            self.video.properties.dimensions, self.dimensions, self.resize
        )
        self.filepath = P.prepare_filepath(
            self.video.filepath.stem, self.filename, self.destdir, "gif"
        )

    def __str__(self) -> str:
        import videoxt.displays

        return super().__str__() + videoxt.displays.gif_request_str(self)
