"""Contains functions used to edit a VideoFileClip or np.ndarray prior to extraction."""
from typing import Optional

import cv2  # type: ignore
import numpy as np
from moviepy.editor import afx  # type: ignore
from moviepy.editor import VideoFileClip, vfx

import videoxt.constants as C


def trim_clip(
    clip: VideoFileClip,
    start_second: Optional[float] = None,
    stop_second: Optional[float] = None,
) -> VideoFileClip:
    """
    Trim a VideoFileClip to a specific time range and return the trimmed clip.

    Args:
    -----
        `clip` (moviepy.editor.VideoFileClip):
            The clip to trim.
        `start_second` (Optional[float]):
            The start time in seconds. If None, the trim will start at the beginning.
        `stop_second` (Optional[float]):
            The stop time in seconds. If None, the clip will be trimmed to the end.

    Returns:
    -----
        `moviepy.editor.VideoFileClip`: The trimmed clip.
    """
    if start_second is None and stop_second is None:
        return clip

    if start_second is None:
        start_second = 0.0

    if stop_second is None:
        stop_second = clip.duration

    return clip.subclip(start_second, stop_second)


def edit_clip_audio(
    clip: VideoFileClip,
    volume: Optional[float] = None,
    normalize: Optional[bool] = None,
) -> VideoFileClip:
    """
    Edit the audio of a VideoFileClip by adjusting its volume and normalizing the
    audio if specified and return the edited clip.

    Args:
    -----
        `clip` (moviepy.editor.VideoFileClip):
            The clip to edit.
        `volume` (Optional[float]):
            The volume multiplier. If None, the volume will not be adjusted.
        `normalize` (Optional[bool]):
            Whether to normalize the audio. If None, the audio will not be normalized.

    Returns:
    -----
        `moviepy.editor.VideoFileClip`: The edited clip.
    """
    if normalize:
        clip = clip.fx(afx.audio_normalize)

    if volume != 1.0:
        clip = clip.volumex(volume)

    return clip


def edit_clip_image(
    clip: VideoFileClip,
    dimensions: Optional[tuple[int, int]] = None,
    rotate: Optional[int] = None,
    monochrome: Optional[bool] = None,
) -> VideoFileClip:
    """
    Edit the image properties of a VideoFileClip by resizing, rotating, and converting
    to monochrome if specified and return the edited clip.

    Args:
    -----
        `clip` (moviepy.editor.VideoFileClip):
            The clip to edit.
        `dimensions` (Optional[tuple[int, int]]):
            The dimensions to resize the clip to. If None, the clip will not be resized.
        `rotate` (Optional[int]):
            The degrees to rotate the clip. If None, the clip will not be rotated.
        `monochrome` (Optional[bool]):
            Whether to convert the clip to monochrome. If None, the black and white
            filter will not be applied.

    Returns:
    -----
        `moviepy.editor.VideoFileClip`: The edited clip.
    """
    if dimensions is not None:
        clip = clip.resize(dimensions)

    if rotate != 0:
        clip = clip.rotate(rotate)

    if monochrome:
        clip = clip.fx(vfx.blackwhite)

    return clip


def edit_clip_motion(
    clip: VideoFileClip,
    speed: Optional[float] = None,
    reverse: Optional[bool] = None,
    bounce: Optional[bool] = None,
) -> VideoFileClip:
    """
    Edit the moving image properties of a VideoFileClip by adjusting its speed,
    reversing, and bouncing if specified and return the edited clip.

    Args:
    -----
        `clip` (moviepy.editor.VideoFileClip):
            The clip to edit.
        `speed` (Optional[float]):
            The speed multiplier. If None, the speed will not be adjusted.
        `reverse` (Optional[bool]):
            Whether to reverse the clip. If None, the clip will not be reversed.
        `bounce` (Optional[bool]):
            Whether to bounce the clip. If None, the clip will not be bounced.

    Returns:
    -----
        `moviepy.editor.VideoFileClip`: The edited clip.
    """
    if reverse:
        clip = clip.fx(vfx.time_mirror)

    if bounce:
        clip = clip.fx(vfx.time_symmetrize)

    if speed != 1.0:
        clip = clip.fx(vfx.speedx, speed)

    return clip


def edit_image(
    image: np.ndarray,
    dimensions: Optional[tuple[int, int]] = None,
    rotate: Optional[int] = None,
    monochrome: Optional[bool] = None,
) -> np.ndarray:
    """
    Edit a numpy.ndarray image by resizing, rotating, and converting to monochrome
    if specified and return the edited image.

    Args:
    -----
        `image` (np.ndarray):
            The image to edit.
        `dimensions` (Optional[tuple[int, int]]):
            The dimensions to resize the image to. If None, the image will not be
            resized.
        `rotate` (Optional[int]):
            The degrees to rotate the image. If None, the image will not be rotated.
        `monochrome` (Optional[bool]):
            Whether to convert the image to monochrome. If None, the black and white
            filter will not be applied.

    Returns:
    -----
        `np.ndarray`: The edited image.
    """
    if dimensions is not None and dimensions != image.shape:
        image = cv2.resize(image, dimensions)

    if rotate != 0 and rotate is not None:
        try:
            rotate_value = C.ROTATION_MAP[rotate]
        except KeyError:
            pass  # XXX: log
        else:
            image = cv2.rotate(image, rotate_value)

    if monochrome:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image
