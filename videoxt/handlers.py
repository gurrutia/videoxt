"""
Contains factories for creating extraction objects and handlers for executing the
extraction process.
"""
from pathlib import Path
from time import perf_counter
from typing import Any

from rich.console import Console

from videoxt.constants import ExtractionMethod
from videoxt.exceptions import VideoXTError
from videoxt.extractors import (
    AudioExtractor,
    ClipExtractor,
    Extractor,
    FramesExtractor,
    GifExtractor,
)
from videoxt.requestors import (
    AudioRequest,
    ClipRequest,
    FramesRequest,
    GifRequest,
    PreparedAudioRequest,
    PreparedClipRequest,
    PreparedFramesRequest,
    PreparedGifRequest,
    PreparedRequest,
    Request,
)
from videoxt.result import Result
from videoxt.video import Video


class ExtractionHandler:
    """
    Handles the extraction process by creating the necessary objects used to perform
    any extraction.

    Attributes:
    -----
        `method` (ExtractionMethod):
            The extraction method Enum to use (e.g., `ExtractionMethod.AUDIO`).

    Public Methods:
    -----
        `execute` -> `Result`:
            Execute the video extraction process and return a `Result` object.
    """

    def __init__(self, method: ExtractionMethod):
        """Set the objects to be used for extraction based on the chosen method."""
        self.method = method
        self.object_factory = ObjectFactory(self.method)

    def execute(
        self,
        filepath: Path | str,
        options: dict[str, Any] | None = None,
        skip_validation: bool = False,
    ) -> Result:
        """
        Make the necessary objects used to perform the extraction and execute the
        extraction process.

        Args:
        -----
            `filepath` (Path | str):
                Path to the video file with extension.
            `options` (dict[str, Any] | None):
                Extraction options specific to the chosen extraction method. If None,
                default options will be used.
            `skip_validation` (bool):
                If True, skips validation of the extraction options. This can slightly
                improve speed, but it is not recommended unless you are sure that the
                options are valid.
        Returns:
        -----
            `Result`: A dataclass containing the extraction details.
        """
        video = self.object_factory.make_video(filepath)
        request = self.object_factory.make_prepared_request(
            video, options, skip_validation
        )
        extractor = self.object_factory.make_extractor(request)
        result = self.object_factory.make_result()

        if request.is_verbose:
            request.verbose_print(title="PreparedRequest")

        result = self._perform_extraction(extractor, result)

        if request.is_verbose:
            result.verbose_print(title="Result")

        return result

    def _perform_extraction(self, extractor: Extractor, result: Result) -> Result:
        """
        Execute the extraction process and return a `Result` object.

        Args:
        -----
            `extractor` (Extractor):
                The extractor object to use.
            `result` (Result):
                The result object to return.

        Returns:
        -----
            `Result`: A dataclass containing the extraction details.
        """
        _timer_start = perf_counter()
        try:
            if self.method == ExtractionMethod.FRAMES:
                extractor.extract()
            else:
                transient_msg = (
                    f"[yellow]Extracting {self.method.value}...[/yellow]\n"
                    "Press [red][bold]Ctrl+C[/red][/bold] to cancel."
                )
                with Console().status(transient_msg):
                    extractor.extract()

        except KeyboardInterrupt:
            result.success = False
            result.message = "Extraction cancelled."

        except VideoXTError as error_msg:
            result.success = False
            result.message = f"Extraction failed: {error_msg}"

        else:
            result.success = True
            result.message = "Extraction successful."

        finally:
            if extractor.request.destpath.exists():
                result.destpath = extractor.request.destpath

            result.elapsed_time = perf_counter() - _timer_start
            return result


class ObjectFactory:
    """
    Factory for creating the necessary objects used to perform any extraction.

    Attributes:
    -----
        `method` (ExtractionMethod):
            The extraction method Enum to use (e.g., `ExtractionMethod.AUDIO`).

    Class Attributes:
    -----
        `REQUEST_MAP` (dict[ExtractionMethod, Type[Request]]):
            Mapping of extraction methods to their corresponding request classes.
        `PREPARED_REQUEST_MAP` (dict[ExtractionMethod, Type[PreparedRequest]]):
            Mapping of extraction methods to their corresponding prepared request
            classes.
        `EXTRACTOR_MAP` (dict[ExtractionMethod, Type[Extractor]]):
            Mapping of extraction methods to their corresponding extractor classes.

    Public Methods:
    -----
        `make_video` -> `Video`:
            Create a `Video` object.
        `make_prepared_request` -> `PreparedRequest`:
            Create a `PreparedRequest` object.
        `make_extractor` -> `Extractor`:
            Create an `Extractor` object.
        `make_result` -> `Result`:
            Create a `Result` object.
    """

    REQUEST_MAP: dict[ExtractionMethod, type[Request]] = {
        ExtractionMethod.AUDIO: AudioRequest,
        ExtractionMethod.CLIP: ClipRequest,
        ExtractionMethod.FRAMES: FramesRequest,
        ExtractionMethod.GIF: GifRequest,
    }
    PREPARED_REQUEST_MAP: dict[ExtractionMethod, type[PreparedRequest]] = {
        ExtractionMethod.AUDIO: PreparedAudioRequest,
        ExtractionMethod.CLIP: PreparedClipRequest,
        ExtractionMethod.FRAMES: PreparedFramesRequest,
        ExtractionMethod.GIF: PreparedGifRequest,
    }
    EXTRACTOR_MAP: dict[ExtractionMethod, type[Extractor]] = {
        ExtractionMethod.AUDIO: AudioExtractor,
        ExtractionMethod.CLIP: ClipExtractor,
        ExtractionMethod.FRAMES: FramesExtractor,
        ExtractionMethod.GIF: GifExtractor,
    }

    def __init__(self, method: ExtractionMethod):
        """Set the objects to be used for extraction based on the chosen method."""
        self.method = method

    def make_video(self, filepath: Path | str) -> Video:
        """
        Use the given video filepath to create a `Video` object.

        Args:
        -----
            `filepath` (Path | str): Path to the video file with extension.

        Returns:
        -----
            `Video`: A dataclass containing the video details.
        """
        return Video(Path(filepath))

    def make_prepared_request(
        self,
        video: Video,
        options: dict[str, Any] | None = None,
        skip_validation: bool = False,
    ) -> PreparedRequest:
        """
        Use the given video and options to create a `PreparedRequest` object.

        Args:
        -----
            `video` (Video):
                The video object to use.
            `options` (dict[str, Any] | None):
                Extraction options specific to the chosen extraction method. If None,
                default options will be used.
            `skip_validation` (bool):
                If True, skips validation of the extraction options. This can slightly
                improve speed, but it is not recommended unless you are sure that the
                options are valid.

        Returns:
        -----
            `PreparedRequest`: A dataclass containing the prepared request details.
        """
        if options is None:
            return self.PREPARED_REQUEST_MAP[self.method](video).prepare()

        if skip_validation:
            return self.PREPARED_REQUEST_MAP[self.method](video, **options).prepare()

        return self.REQUEST_MAP[self.method](**options).validate().prepare(video)

    def make_extractor(self, prepared_request: PreparedRequest) -> Extractor:
        """
        Use the given prepared request to create an `Extractor` object.

        Args:
        -----
            `prepared_request` (PreparedRequest): A type of prepared request to use.

        Returns:
        -----
            `Extractor`: A type of extractor object.
        """
        return self.EXTRACTOR_MAP[self.method](prepared_request)

    def make_result(self) -> Result:
        """Create and return a `Result` object with the chosen extraction method."""
        return Result(method=self.method.value)
