"""Contains custom exceptions raised by videoxt."""


class VideoXTError(Exception):
    """A videoxt specific error occurred."""

    pass


class InvalidExtractionMethod(VideoXTError):
    """An invalid extraction method was requested."""

    pass


class ClosedVideoCaptureError(VideoXTError):
    """A `cv2.VideoCapture` was unexpectedly closed."""

    pass


class VideoValidationError(VideoXTError):
    """A video file failed a validation step."""

    pass


class PreparationError(VideoXTError):
    """An error occurred while preparing a request."""

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


class GifWriteError(VideoXTError):
    """An error occurred while writing a gif to file."""

    pass


class AudioWriteError(VideoXTError):
    """An error occurred while writing an audio file."""

    pass


class ClipWriteError(VideoXTError):
    """An error occurred while writing a clip to file."""

    pass


class BuildImagePathError(VideoXTError):
    """An error occurred while building an image path."""

    pass
