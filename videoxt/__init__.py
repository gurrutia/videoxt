"""
/* VideoXT */

A simple library and CLI tool for extracting audio, individual frames, short clips and
GIFs from videos.

Contents:
-----
- `extract`: Extract audio, individual frames, short clips and GIFs from videos.
- `extract_audio`: Extract audio from a video file.
- `extract_clip`: Extract a short clip from a video file as `mp4`.
- `extract_frames`: Extract individual frames from a video and save them as images.
- `extract_gif`: Create a GIF from a video between two specified points.

Basic Usage:
-----
>>> import videoxt as vxt
>>> video_filepath = "path/to/video.mp4"  # or pathlib.Path("path/to/video.mp4")

# Extract all audio.
>>> vxt.extract("audio", video_filepath)  # or...
>>> vxt.extract_audio(video_filepath)

# Save every 30th frame of the video to disk as an image.
>>> vxt.extract_frames(
...     video_filepath,
...     capture_rate=30
... )

# Extract a clip between 12:29 and 12:34 from the video.
>>> vxt.extract_clip(
...     video_filepath,
...     start_time="12:29",
...     stop_time="12:34"
... )

# Extract a GIF of the first 2 seconds of the video that bounces back and forth.
>>> vxt.extract_gif(
...     video_filepath,
...     stop_time=2,
...     bounce=True
... )
"""

# flake8: noqa

from videoxt.api import (
    extract,
    extract_audio,
    extract_clip,
    extract_frames,
    extract_gif,
)
