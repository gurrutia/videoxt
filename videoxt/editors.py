"""Contains functions used to edit a VideoFileClip or np.ndarray prior to extraction."""
from typing import Optional

import cv2  # type: ignore
import numpy as np
from moviepy.editor import afx  # type: ignore
from moviepy.editor import VideoFileClip, vfx

import videoxt.constants as C


def trim_clip(
    clip: VideoFileClip, start_second: Optional[float], stop_second: Optional[float]
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
    clip: VideoFileClip, volume: float, normalize: bool
) -> VideoFileClip:
    """
    Edit the audio of a VideoFileClip by adjusting its volume and normalizing the
    audio if specified and return the edited clip.

    Args:
    -----
        `clip` (moviepy.editor.VideoFileClip):
            The clip to edit.
        `volume` (float):
            The volume multiplier.
        `normalize` (bool):
            Whether to normalize the audio.

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
    clip: VideoFileClip, dimensions: tuple[int, int], rotate: int, monochrome: bool
) -> VideoFileClip:
    """
    Edit the image properties of a VideoFileClip by resizing, rotating, and converting
    to monochrome if specified and return the edited clip.

    Args:
    -----
        `clip` (moviepy.editor.VideoFileClip):
            The clip to edit.
        `dimensions` (tuple[int, int]):
            The dimensions to resize the clip to.
        `rotate` (int):
            The degrees to rotate the clip.
        `monochrome` (bool):
            Whether to convert the clip to monochrome.

    Returns:
    -----
        `moviepy.editor.VideoFileClip`: The edited clip.
    """
    clip = clip.resize(dimensions)

    if rotate != 0:
        clip = clip.rotate(rotate)

    if monochrome:
        clip = clip.fx(vfx.blackwhite)

    return clip


def edit_clip_motion(
    clip: VideoFileClip,
    speed: Optional[float],
    reverse: Optional[bool],
    bounce: Optional[bool],
) -> VideoFileClip:
    """
    Edit the moving image properties of a VideoFileClip by adjusting its speed,
    reversing, and bouncing if specified and return the edited clip.

    Args:
    -----
        `clip` (VideoFileClip):
            The clip to edit.
        `speed` (Optional[float]):
            The speed multiplier.
        `reverse` (Optional[bool]):
            Whether to reverse the clip.
        `bounce` (Optional[bool]):
            Whether to bounce the clip.

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
    image: np.ndarray, dimensions: tuple[int, int], rotate: int, monochrome: bool
) -> np.ndarray:
    """
    Edit a numpy.ndarray image by resizing, rotating, and converting to monochrome
    if specified and return the edited image.

    Args:
    -----
        `image` (np.ndarray):
            The image to edit.
        `dimensions` (tuple[int, int]):
            The dimensions to resize the image to.
        `rotate` (int):
            The degrees to rotate the image.
        `monochrome` (bool):
            Whether to convert the image to monochrome.

    Returns:
    -----
        `np.ndarray`: The edited image.
    """
    image = cv2.resize(image, dimensions)

    if rotate != 0:
        image = cv2.rotate(image, C.ROTATION_MAP[rotate])

    if monochrome:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image
