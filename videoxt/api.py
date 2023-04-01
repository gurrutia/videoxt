import typing as t
from pathlib import Path

import videoxt.extractors as E
import videoxt.requestors as R


def extract_audio(filepath: Path, **kwargs: t.Dict[str, t.Any]) -> None:
    """Extract audio from a video file.

    Args:
    ------------
        `filepath` (Path, str) :
            Path to the video file.
        `start_time` (float, str) :
            Time to start extraction. Can be a float representing seconds or
            a string in the format `HH:MM:SS`, `H:MM:SS`, `MM:SS`, or `M:SS`.
        `stop_time` (float, str) :
            Time to stop extraction. Can be a float representing seconds or
            a string in the format `HH:MM:SS`, `H:MM:SS`, `MM:SS`, or `M:SS`.
        `fps` (float) :
            Override the video's frames per second. If `None`, the video fps is used.
        `destdir` (Path, str) :
            Directory to save the media to. If `None`, the video directory is used.
        `filename` (str) :
            Filename of the resulting media without extension. If `None`, the video filename is used.
        `verbose` (bool) :
            If `True`, prints extraction details to console prior to extraction.
        `audio_format` (str) :
            Audio format to save as.
            Valid values are `mp3`, `wav`, `ogg`, or `m4a`.
            Defaults to `mp3`.
        `speed` (float) :
            Increase or decrease the speed of the audio playback by a factor of `n`.
        `volume` (float) :
            Increase or decrease the audio volume by a factor of `n`.
        `bounce` (bool) :
            If `True`, bounces the audio back and forth. Can be used in conjunction with `reverse`.
        `reverse` (bool) :
            If `True`, reverses the audio. Can be used in conjunction with `bounce`.
        `normalize` (bool) :
            If `True`, normalizes the audio output to a maximum of 0dB.

    Note: Unrecognized arguments are ignored.
    """
    E.extraction_factory(filepath, R.AudioRequest, E.AudioExtractor, **kwargs)


def extract_clip(filepath: Path, **kwargs: t.Dict[str, t.Any]) -> None:
    """Extract a clip of a video file. Only supports `mp4` output.

    Args:
    ------------
        `filepath` (Path, str) :
            Path to the video file.
        `start_time` (float, str) :
            Time to start extraction. Can be a float representing seconds or
            a string in the format `HH:MM:SS`, `H:MM:SS`, `MM:SS`, or `M:SS`.
        `stop_time` (float, str) :
            Time to stop extraction. Can be a float representing seconds or
            a string in the format `HH:MM:SS`, `H:MM:SS`, `MM:SS`, or `M:SS`.
        `fps` (float) :
            Override the video's frames per second. If `None`, the video fps is used.
        `destdir` (Path, str) :
            Directory to save the media to. If `None`, the video directory is used.
        `filename` (str) :
            Filename of the resulting media without extension. If `None`, the video filename is used.
        `verbose` (bool) :
            If `True`, prints extraction details to console prior to extraction.
        `resize` (float) :
            Resize the clip by a factor of `n`.
        `rotate` (int) :
            Rotate the clip by `n` degrees.
            Valid values are `0`, `90`, `180`, or `270`.
        `speed` (float) :
            Increase or decrease the speed of the clip by a factor of `n`.
        `volume` (float) :
            Increase or decrease the audio volume by a factor of `n`.
        `monochrome` (bool) :
            If `True`, applies a black and white filter to the clip.
        `bounce` (bool) :
            If `True`, bounces the clip back and forth. Can be used in conjunction with `reverse`.
        `reverse` (bool) :
            If `True`, reverses the clip. Can be used in conjunction with `bounce`.
        `normalize` (bool) :
            If `True`, normalizes the audio output to a maximum of 0dB.
        `dimensions` (Tuple[int, int]) :
            Resize the clip to the specified dimensions `(width, height)`.

    Note: Unrecognized arguments are ignored.
    """
    E.extraction_factory(filepath, R.ClipRequest, E.ClipExtractor, **kwargs)


def extract_frames(filepath: Path, **kwargs: t.Dict[str, t.Any]) -> None:
    """Extract individual frames from a video and save them as images.

    Args:
    ------------
        `filepath` (Path, str) :
            Path to the video file.
        `start_time` (float, str) :
            Time to start extraction. Can be a float representing seconds or
            a string in the format `HH:MM:SS`, `H:MM:SS`, `MM:SS`, or `M:SS`.
        `stop_time` (float, str) :
            Time to stop extraction. Can be a float representing seconds or
            a string in the format `HH:MM:SS`, `H:MM:SS`, `MM:SS`, or `M:SS`.
        `fps` (float) :
            Override the video's frames per second. If `None`, the video fps is used.
        `destdir` (Path, str) :
            Directory to save the media to. If `None`, the video directory is used.
        `filename` (str) :
            Filename of the resulting media without extension. If `None`, the video filename is used.
        `verbose` (bool) :
            If `True`, prints extraction details to console prior to extraction.
        `image_format` (str) :
            Image format to save as.
            Valid values are `jpg`, `jpeg`, `png`,`webp`, `bmp`, `dib`, `tif`, or `tiff`.
            Defaults to `jpg`.
        `capture_rate` (int) :
            Capture every nth video frame. Default is 1, which captures every frame.
        `resize` (float) :
            Resize the images by a factor of `n`.
        `rotate` (int) :
            Rotate the images by `n` degrees.
            Valid values are `0`, `90`, `180`, or `270`.
        `monochrome` (bool) :
            If `True`, applies a black and white filter to the images.
        `dimensions` (Tuple[int, int]) :
            Resize the images to the specified dimensions `(width, height)`.

    Note: Unrecognized arguments are ignored.
    """
    E.extraction_factory(filepath, R.FramesRequest, E.FramesExtractor, **kwargs)


def extract_gif(filepath: Path, **kwargs: t.Dict[str, t.Any]) -> None:
    """Create a GIF between two points in a video.

    Args:
    ------------
        `filepath` (Path, str) :
            Path to the video file.
        `start_time` (float, str) :
            Time to start extraction. Can be a float representing seconds or
            a string in the format `HH:MM:SS`, `H:MM:SS`, `MM:SS`, or `M:SS`.
        `stop_time` (float, str) :
            Time to stop extraction. Can be a float representing seconds or
            a string in the format `HH:MM:SS`, `H:MM:SS`, `MM:SS`, or `M:SS`.
        `fps` (float) :
            Override the video's frames per second. If `None`, the video fps is used.
        `destdir` (Path, str) :
            Directory to save the media to. If `None`, the video directory is used.
        `filename` (str) :
            Filename of the resulting media without extension. If `None`, the video filename is used.
        `verbose` (bool) :
            If `True`, prints extraction details to console prior to extraction.
        `resize` (float) :
            Resize the gif by a factor of `n`.
        `rotate` (int) :
            Rotate the gif by `n` degrees.
            Valid values are `0`, `90`, `180`, or `270`.
        `speed` (float) :
            Increase or decrease the speed of the gif by a factor of `n`.
        `monochrome` (bool) :
            If `True`, applies a black and white filter to the gif.
        `bounce` (bool) :
            If `True`, bounces the gif back and forth. Can be used in conjunction with `reverse`.
        `reverse` (bool) :
            If `True`, reverses the gif. Can be used in conjunction with `bounce`.
        `dimensions` (Tuple[int, int]) :
            Resize the gif to the specified dimensions `(width, height)`.

    Note: Unrecognized arguments are ignored.
    """
    E.extraction_factory(filepath, R.GifRequest, E.GifExtractor, **kwargs)
