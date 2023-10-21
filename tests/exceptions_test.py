import pytest

from videoxt.exceptions import (
    ClosedVideoCaptureError,
    FrameReadError,
    FrameWriteError,
    InvalidExtractionMethod,
    NoAudioError,
    RequestPreparationError,
    ValidationError,
    VideoCaptureSetError,
    VideoValidationError,
    VideoXTError,
)


@pytest.mark.parametrize(
    "exception",
    [
        ClosedVideoCaptureError,
        FrameReadError,
        FrameWriteError,
        InvalidExtractionMethod,
        NoAudioError,
        RequestPreparationError,
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
