"""Configuration file containing shared pytest fixtures."""
import os
import shutil
import typing as t
from pathlib import Path

import cv2
import numpy as np
import pytest
from moviepy.editor import AudioClip
from moviepy.editor import VideoClip


@pytest.fixture(scope="session")
def session_tmp_dir() -> Path:
    """Create a temporary directory for the session and yield its path.

    Yields:
        Path: The path of the temporary directory.
    """
    temp_dir = Path("tmp")
    temp_dir.mkdir(exist_ok=True)
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def video_properties(session_tmp_dir: Path) -> t.Dict[str, t.Any]:
    """Create a dictionary of properties for a temporary video. Only some properties are
    used to create the video. The rest are used to test for equality.

    Args:
        session_tmp_dir (Path): The path of the temporary directory for the session.

    Yields:
        t.Dict[str, t.Any]: A dictionary of properties for the temporary video.
    """
    return {
        "video_file_path": session_tmp_dir / "tmp.video.mp4",
        "filename": "tmp.video",
        "frame_width": 640,
        "frame_height": 480,
        "dimensions": (640, 480),
        "fps": 10.0,
        "duration_seconds": 2.0,
        "duration_timestamp": "0:00:02",
        "frame_count": 20,
        "suffix": "mp4",
        "codec": "libx264",
        "audio_codec": "aac",
    }


@pytest.fixture(scope="session")
def tmp_video_filepath(video_properties: t.Dict[str, t.Any]) -> Path:
    """Create a temporary video file and yield its path.

    Args:
        video_properties (t.Dict[str, t.Any]): A dictionary of properties for the temporary video.

    Yields:
        Path: Filepath of the temporary video file.
    """

    def make_frame(time: float) -> np.ndarray:
        """Generate a single video frame."""
        frame_num = int(time * video_properties["fps"]) + 1
        frame = np.zeros(
            (video_properties["frame_height"], video_properties["frame_width"], 3),
            dtype=np.uint8,
        )
        text = f"Frame: {frame_num}"
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame

    def make_audio(time: float) -> float:
        """Generate synthetic audio for the length of the video."""
        return np.sin(2 * np.pi * 440 * time)

    # Generate the video and set the audio
    video = VideoClip(make_frame, duration=video_properties["duration_seconds"])
    audio = AudioClip(make_audio, duration=video_properties["duration_seconds"])
    video = video.set_audio(audio)

    # Write the video to disk
    video.write_videofile(
        str(video_properties["video_file_path"]),
        codec=video_properties["codec"],
        audio_codec=video_properties["audio_codec"],
        fps=video_properties["fps"],
    )

    # Yield the filepath of the temporary video file then delete it
    yield video_properties["video_file_path"]

    # Delete the temporary video file
    if video_properties["video_file_path"].exists():
        os.remove(video_properties["video_file_path"])


@pytest.fixture(scope="session")
def tmp_text_filepath(session_tmp_dir: Path) -> Path:
    """Create a temporary text file in the temporary directory and yield its path.

    `session_tmp_dir` is a fixture that creates a temporary directory for the session.

    Yields:
        Path: Filepath of the temporary text file.
    """
    tmp_filepath = session_tmp_dir / "tmp.text.txt"
    content = "This is a temporary text file."
    with open(tmp_filepath, "w") as f:
        f.write(content)

    yield tmp_filepath

    if tmp_filepath.exists():
        os.remove(tmp_filepath)
