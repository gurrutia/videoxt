class VideoXTError(Exception):
    """A videoxt specific error occurred."""

    pass


class InvalidExtractionMethod(VideoXTError):
    """An invalid extraction method was requested."""

    pass


class ClosedVideoCaptureError(VideoXTError):
    """
    An error occurred attempting to open or maintain a `cv2.VideoCapture` in an open
    state.
    """

    pass


class VideoValidationError(VideoXTError):
    """A video file failed a validation step."""

    pass


class RequestPreparationError(VideoXTError):
    """An error occurred while preparing a `PreparedRequest` object."""

    pass


class ValidationError(VideoXTError):
    """A user input validation step failed."""

    pass


class NoAudioError(VideoXTError):
    """A video has no audio and it is required for the operation."""

    pass


class FrameReadError(VideoXTError):
    """An error occurred while reading a frame from a video using `cv2`."""

    pass


class VideoCaptureSetError(VideoXTError):
    """An error occurred while setting a VideoCapture property using `cv2`."""

    pass


class FrameWriteError(VideoXTError):
    """An error occurred while writing a frame to file using `cv2`."""

    pass
