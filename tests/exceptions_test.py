import pytest

from videoxt.exceptions import (
    AudioWriteError,
    BuildImagePathError,
    ClipWriteError,
    ClosedVideoCaptureError,
    FrameReadError,
    FrameWriteError,
    GifWriteError,
    InvalidExtractionMethod,
    NoAudioError,
    PreparationError,
    ValidationError,
    VideoCaptureSetError,
    VideoValidationError,
    VideoXTError,
)


@pytest.mark.parametrize(
    "exception",
    [
        AudioWriteError,
        BuildImagePathError,
        ClipWriteError,
        ClosedVideoCaptureError,
        FrameReadError,
        FrameWriteError,
        GifWriteError,
        InvalidExtractionMethod,
        NoAudioError,
        PreparationError,
        ValidationError,
        VideoCaptureSetError,
        VideoValidationError,
        VideoXTError,
    ],
)
def test_errors(exception):
    with pytest.raises(exception) as exc_info:
        raise exception("Custom error message")

    assert str(exc_info.value) == "Custom error message"
