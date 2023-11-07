"""Simple interface for extracting audio, clips, frames, and gifs from a video file."""
from pathlib import Path
from typing import Any

from videoxt.constants import ExtractionMethod
from videoxt.exceptions import InvalidExtractionMethod
from videoxt.handlers import ExtractionHandler
from videoxt.result import Result


def extract(
    method: str,
    filepath: Path | str,
    skip_validation: bool = False,
    **options: dict[str, Any] | None,
) -> Result:
    """
    Extract audio, individual frames, short clips and GIFs from videos.

    See the documentation for list of options, or:

    - `extract_audio`: Extract audio from a video file.
    - `extract_clip`: Extract a short clip from a video file as `mp4`.
    - `extract_frames`: Extract individual frames from a video and save them as images.
    - `extract_gif`: Create a GIF from a video between two specified points.

    Args:
    -----
        `method` (str):
            The extraction method to use ("audio", "clip", "frames", "gif").
        `filepath` (Path | str):
            Path to the video file with extension.
        `skip_validation` (bool):
            If True, skips validation of the extraction options. This can slightly
            improve speed, but it is not recommended unless you are sure that the
            options are valid.
        `**options` (dict[str, Any] | None):
            Extraction options specific to the chosen extraction method.

    Returns:
    -----
        `Result`: A dataclass containing the extraction details.

    Raises:
    -----
        `InvalidExtractionMethod`:
            If the extraction method is neither "audio", "clip", "frames", nor "gif".
    """
    try:
        method_enum = ExtractionMethod[method.upper()]

    except KeyError:
        raise InvalidExtractionMethod(
            f"Invalid extraction method: {method}. "
            f"Choices are {', '.join([em.value for em in ExtractionMethod])}."
        )

    else:
        handler = ExtractionHandler(method_enum)
        return handler.execute(filepath, options, skip_validation=skip_validation)


def extract_audio(
    filepath: Path | str,
    start_time: float | int | str = 0,
    stop_time: float | int | str | None = None,
    destdir: Path | str | None = None,
    filename: str | None = None,
    verbose: bool = False,
    overwrite: bool = False,
    fps: float | None = None,
    audio_format: str = "mp3",
    speed: float = 1,
    bounce: bool = False,
    reverse: bool = False,
    volume: float = 1,
    normalize: bool = False,
) -> Result:
    """
    Extract audio from a video file.

    Args:
    -----
        `filepath` (Path | str):
            Path to the video file with extension.
        `start_time` (float | int | str):
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
        `verbose` (bool):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `audio_format` (str):
            Set the extracted audio file format. Defaults to 'mp3' if not specified.
            See: `videoxt.constants.SUPPORTED_AUDIO_FORMATS`.
        `speed` (float):
            Set the speed of the extracted audio. A value of 0.5 will halve the speed of
            the extracted audio. Defaults to 1.0 if not specified (no change).
        `bounce` (bool):
            If True, bounce the extracted audio bommerang-style. Defaults to False if
            not specified.
        `reverse` (bool):
            If True, reverse the extracted audio. Defaults to False if not specified.
        `volume` (float):
            Set the volume of the extracted audio. A value of 0.5 will halve the volume
            of the extracted audio. Defaults to 1.0 if not specified (no change).
        `normalize` (bool):
            If True, normalize the audio. Normalization adjusts the gain of the audio to
            ensure consistent levels, preventing distortion and enhancing clarity in
            some cases. Defaults to False if not specified.

    Returns:
    -----
        `Result`: A dataclass containing the extraction details.
    """
    options = {
        "start_time": start_time,
        "stop_time": stop_time,
        "destdir": destdir,
        "filename": filename,
        "verbose": verbose,
        "overwrite": overwrite,
        "fps": fps,
        "audio_format": audio_format,
        "speed": speed,
        "bounce": bounce,
        "reverse": reverse,
        "volume": volume,
        "normalize": normalize,
    }

    handler = ExtractionHandler(ExtractionMethod.AUDIO)
    return handler.execute(filepath, options)


def extract_clip(
    filepath: Path | str,
    start_time: float | int | str = 0,
    stop_time: float | int | str | None = None,
    destdir: Path | str | None = None,
    filename: str | None = None,
    verbose: bool = False,
    overwrite: bool = False,
    fps: float | None = None,
    dimensions: tuple[int, int] | None = None,
    resize: float = 1.0,
    rotate: int = 0,
    speed: float = 1.0,
    bounce: bool = False,
    reverse: bool = False,
    monochrome: bool = False,
    volume: float = 0,
    normalize: bool = False,
) -> Result:
    """
    Extract a clip from a video file as `mp4`.

    Recommended usage: Set a short extraction range. The process can be slow for long
    or high-resolution videos.

    Args:
    -----
        `filepath` (Path | str):
            Path to the video file with extension.
        `start_time` (float | int | str):
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
        `verbose` (bool):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool):
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
        `resize` (float):
            Resize the dimensions of the clip by a factor of `n`. A value of 0.5
            will halve the dimensions. If you specify `dimensions`, `resize` will apply
            to the dimensions you specify. Defaults to 1.0 if not specified (no change).
        `rotate` (int):
            Rotate the clip by `n` degrees. Allowed values: 0, 90, 180 or 270. Defaults
            to 0 if not specified (no change).
        `speed` (float):
            Set the speed of the extracted clip. A value of 0.5 will halve the playback
            speed of the clip. Defaults to 1.0 if not specified (no change).
        `bounce` (bool):
            If True, bounce the extracted clip bommerang-style. Defaults to False if
            not specified.
        `reverse` (bool):
            If True, reverse the extracted clip. Defaults to False if not specified.
        `monochrome` (bool):
            If True, apply a black-and-white filter to the clip. Defaults to False if
            not specified.
        `volume` (float):
            Set the volume of the extracted clip's audio. A value of 0.5 will halve the
            volume of the clip's audio. Defaults to 1.0 if not specified (no change).
        `normalize` (bool):
            If True, normalize the audio. Normalization adjusts the gain of the audio to
            ensure consistent levels, preventing distortion and enhancing clarity in
            some cases. Defaults to False if not specified.

    Returns:
    -----
        `Result`: A dataclass containing the extraction details.
    """
    options = {
        "start_time": start_time,
        "stop_time": stop_time,
        "destdir": destdir,
        "filename": filename,
        "verbose": verbose,
        "overwrite": overwrite,
        "fps": fps,
        "dimensions": dimensions,
        "resize": resize,
        "rotate": rotate,
        "speed": speed,
        "bounce": bounce,
        "reverse": reverse,
        "monochrome": monochrome,
        "volume": volume,
        "normalize": normalize,
    }

    handler = ExtractionHandler(ExtractionMethod.CLIP)
    return handler.execute(filepath, options)


def extract_frames(
    filepath: Path | str,
    start_time: float | int | str = 0,
    stop_time: float | int | str | None = None,
    destdir: Path | str | None = None,
    filename: str | None = None,
    verbose: bool = False,
    overwrite: bool = False,
    fps: float | None = None,
    image_format: str = "jpg",
    capture_rate: int = 1,
    dimensions: tuple[int, int] | None = None,
    resize: float = 1.0,
    rotate: int = 0,
    monochrome: bool = False,
) -> Result:
    """
    Extract individual frames from a video and save them to disk as images.

    The images are saved to a directory named after the video file, or to a directory
    you specify.

    Args:
    -----
        `filepath` (Path | str):
            Path to the video file with extension.
        `start_time` (float | int | str):
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
        `verbose` (bool):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool):
            If True, permits overwriting the destination path if the file or directory
            already exists. Defaults to False if not specified.
        `fps` (float | None):
            Override the frames per second (fps) value obtained from `cv2` when reading
            the video. This value is used to set the start and stop frames for the
            extraction range. This option should be used only in rare cases where `cv2`
            fails to accurately read the fps. If not specified, it defaults to the fps
            of the video as read by `cv2`.
        `image_format` (str):
            Set the extracted image file format. Defaults to 'jpg' if not specified.
            See: `videoxt.constants.SUPPORTED_IMAGE_FORMATS`.
        `capture_rate` (int):
            Capture every Nth video frame. Defaults to 1 if not specified, which
            extracts every frame within the extraction range.
        `dimensions` (tuple[int, int] | None):
            Specify the dimensions (frame width, frame height) of the images. Defaults
            to the video dimensions if not specified.
        `resize` (float):
            Resize the dimensions of the images by a factor of `n`. A value of 0.5
            will halve the dimensions. If you specify `dimensions`, `resize` will apply
            to the dimensions you specify. Defaults to 1.0 if not specified (no change).
        `rotate` (int):
            Rotate the images by `n` degrees. Allowed values: 0, 90, 180 or 270.
            Defaults to 0 if not specified (no change).
        `monochrome` (bool):
            If True, apply a black-and-white filter to the images. Defaults to False if
            not specified.

    Returns:
    -----
        `Result`: A dataclass containing the extraction details.
    """
    options = {
        "start_time": start_time,
        "stop_time": stop_time,
        "destdir": destdir,
        "filename": filename,
        "verbose": verbose,
        "overwrite": overwrite,
        "fps": fps,
        "image_format": image_format,
        "capture_rate": capture_rate,
        "dimensions": dimensions,
        "resize": resize,
        "rotate": rotate,
        "monochrome": monochrome,
    }

    handler = ExtractionHandler(ExtractionMethod.FRAMES)
    return handler.execute(filepath, options)


def extract_gif(
    filepath: Path | str,
    start_time: float | int | str = 0,
    stop_time: float | int | str | None = None,
    destdir: Path | str | None = None,
    filename: str | None = None,
    verbose: bool = False,
    overwrite: bool = False,
    fps: float | None = None,
    dimensions: tuple[int, int] | None = None,
    resize: float = 1.0,
    rotate: int = 0,
    speed: float = 1.0,
    bounce: bool = False,
    reverse: bool = False,
    monochrome: bool = False,
) -> Result:
    """
    Extract a GIF from a video file.

    Recommended usage: Set a short extraction range. The process can be slow for long
    or high-resolution videos.

    Args:
    -----
        `filepath` (Path | str):
            Path to the video file with extension.
        `start_time` (float | int | str):
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
        `verbose` (bool):
            If True, the prepared request and extraction results will be printed as JSON
            to console. Defaults to False if not specified.
        `overwrite` (bool):
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
        `resize` (float):
            Resize the dimensions of the gif by a factor of `n`. A value of 0.5
            will halve the dimensions. If you specify `dimensions`, `resize` will apply
            to the dimensions you specify. Defaults to 1.0 if not specified (no change).
        `rotate` (int):
            Rotate the gif by `n` degrees. Allowed values: 0, 90, 180 or 270. Defaults
            to 0 if not specified (no change).
        `speed` (float):
            Set the speed of the extracted gif. A value of 0.5 will halve the playback
            speed of the gif. Defaults to 1.0 if not specified (no change).
        `bounce` (bool):
            If True, bounce the extracted gif bommerang-style. Defaults to False if
            not specified.
        `reverse` (bool):
            If True, reverse the extracted gif. Defaults to False if not specified.
        `monochrome` (bool):
            If True, apply a black-and-white filter to the gif. Defaults to False if
            not specified.

    Returns:
    -----
        `Result`:
            A Result object containing the result of the extraction process.
    """
    options = {
        "start_time": start_time,
        "stop_time": stop_time,
        "destdir": destdir,
        "filename": filename,
        "verbose": verbose,
        "overwrite": overwrite,
        "fps": fps,
        "dimensions": dimensions,
        "resize": resize,
        "rotate": rotate,
        "speed": speed,
        "bounce": bounce,
        "reverse": reverse,
        "monochrome": monochrome,
    }

    handler = ExtractionHandler(ExtractionMethod.GIF)
    return handler.execute(filepath, options)
