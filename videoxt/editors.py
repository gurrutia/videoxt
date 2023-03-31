"""Functions used to edit VideoFileClip objects and np.ndarray (image) objects."""
import typing as t

import cv2  # type: ignore
import numpy as np
from moviepy.editor import afx  # type: ignore
from moviepy.editor import vfx
from moviepy.editor import VideoFileClip

import videoxt.constants as C


def trim_clip(
    clip: VideoFileClip, start_second: float, stop_second: float
) -> VideoFileClip:
    return clip.subclip(start_second, stop_second)


def edit_clip_audio(
    clip: VideoFileClip, volume: float, normalize: bool
) -> VideoFileClip:
    """Edit VideoFileClip audio. The parameters match those in AudioRequest object."""
    if normalize:
        clip = clip.fx(afx.audio_normalize)

    if volume != 1.0:
        clip = clip.volumex(volume)

    return clip


def edit_clip_image(
    clip: VideoFileClip, dimensions: t.Tuple[int, int], rotate: int, monochrome: bool
) -> VideoFileClip:
    clip = clip.resize(dimensions)

    if rotate != 0:
        clip = clip.rotate(rotate)

    if monochrome:
        clip = clip.fx(vfx.blackwhite)

    return clip


def edit_clip_motion(
    clip: VideoFileClip, speed: float, reverse: bool, bounce: bool
) -> VideoFileClip:
    if reverse:
        clip = clip.fx(vfx.time_mirror)

    if bounce:
        clip = clip.fx(vfx.time_symmetrize)

    if speed != 1.0:
        clip = clip.fx(vfx.speedx, speed)

    return clip


def edit_image(
    image: np.ndarray, dimensions: t.Tuple[int, int], rotate: int, monochrome: bool
) -> np.ndarray:
    image = cv2.resize(image, dimensions)

    if rotate != 0:
        image = cv2.rotate(image, C.ROTATION_MAP[rotate])

    if monochrome:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image
