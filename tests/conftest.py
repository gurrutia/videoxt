"""Pytest configuration file containing shared fixtures."""
import os
import shutil
from collections.abc import Generator
from datetime import timedelta
from pathlib import Path
from typing import Any

import cv2  # type: ignore
import numpy as np
import pytest
from moviepy.editor import AudioClip, VideoClip  # type: ignore


@pytest.fixture(scope="session")
def fixture_tmp_dir() -> Generator[Path, None, None]:
    """
    Create a temporary directory for the session and yield its path.

    Yields:
    -----
        `Generator[Path, None, None]`:
            A generator that yields the path to the temporary directory.
    """
    temp_dir = Path("tmp")
    temp_dir.mkdir(exist_ok=True)
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def fixture_tmp_video_properties(fixture_tmp_dir: Path) -> dict[str, Any]:
    """
    Returns a dictionary of video properties containing values used to create a valid
    temporary video file in `tmp_video_filepath`, and used as expected values for tests.

    Args:
    -----
        `fixture_tmp_dir` (pathlib.Path):
            A fixture that creates a temporary directory for the session.

    Returns:
    -----
        `dict[str, Any]`: A dictionary of properties for the temporary video.
    """
    return {
        "video_file_path": fixture_tmp_dir / "tmp.video.mp4",
        "filename": "tmp.video",
        "audio_codec": "aac",
        "codec": "libx264",
        "dimensions": (640, 480),
        "duration": timedelta(seconds=2),
        "duration_seconds": 2,
        "duration_timestamp": "0:00:02",
        "fps": 10.0,
        "frame_count": 20,
        "frame_height": 480,
        "frame_width": 640,
        "has_audio": True,
    }


@pytest.fixture(scope="session")
def fixture_tmp_video_filepath(
    fixture_tmp_video_properties: dict[str, Any]
) -> Generator[Path, None, None]:
    """
    Create a temporary video file and yield its path.

    Args:
    -----
        `fixture_tmp_video_properties` (dict[str, Any]):
            A fixture that returns a dictionary of properties for the temporary video.

    Yields:
    -----
        `Generator[Path, None, None]`:
            A generator that yields the path to the temporary video file.
    """

    def make_frame(time: float) -> np.ndarray:
        """Generate mock frames for the length of the video."""
        frame_num = int(time * fixture_tmp_video_properties["fps"]) + 1
        frame = np.zeros(
            (
                fixture_tmp_video_properties["frame_height"],
                fixture_tmp_video_properties["frame_width"],
                3,
            ),
            dtype=np.uint8,
        )
        text = f"Frame: {frame_num}"
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame

    def make_audio(time: float) -> float:
        """Generate mock audio for the length of the video."""
        return np.sin(2 * np.pi * 440 * time)

    # Generate the video and set the audio
    video = VideoClip(
        make_frame, duration=fixture_tmp_video_properties["duration_seconds"]
    )
    audio = AudioClip(
        make_audio, duration=fixture_tmp_video_properties["duration_seconds"]
    )
    video = video.set_audio(audio)

    # Write the video to disk
    video.write_videofile(
        str(fixture_tmp_video_properties["video_file_path"]),
        codec=fixture_tmp_video_properties["codec"],
        audio_codec=fixture_tmp_video_properties["audio_codec"],
        fps=fixture_tmp_video_properties["fps"],
    )

    # Yield the filepath of the temporary video file then delete it
    yield fixture_tmp_video_properties["video_file_path"]

    # Delete the temporary video file
    if fixture_tmp_video_properties["video_file_path"].exists():
        os.remove(fixture_tmp_video_properties["video_file_path"])


@pytest.fixture(scope="session")
def fixture_tmp_video_filepath_zero_seconds() -> Generator[Path, None, None]:
    """
    Generate a temporary 'mp4' video file and provide its path. This file is invalid
    due to its 0-second duration, absence of audio, and lack of frames.

    Yields:
    -----
        `Generator[Path, None, None]`:
            A generator that yields the path to the temporary video file.
    """
    video_file_path = Path("tmp") / "tmp.invalid.video.mp4"

    # Generate the video and set the audio
    video = VideoClip(lambda t: np.zeros((480, 640, 3), dtype=np.uint8), duration=0)
    video.write_videofile(str(video_file_path), fps=10)

    yield video_file_path

    # Delete the temporary video file
    if video_file_path.exists():
        os.remove(video_file_path)


@pytest.fixture(scope="session")
def fixture_tmp_text_filepath(fixture_tmp_dir: Path) -> Generator[Path, None, None]:
    """
    Create a temporary text file in the temporary directory and yield its path.

    Yields:
    -----
        `Generator[Path, None, None]`:
            A generator that yields the path to the temporary text file.
    """
    tmp_filepath = fixture_tmp_dir / "tmp.text.txt"
    content = "This is a temporary text file."
    with open(tmp_filepath, "w") as f:
        f.write(content)

    yield tmp_filepath

    if tmp_filepath.exists():
        os.remove(tmp_filepath)
