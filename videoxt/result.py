"""Containers for extraction results."""
from dataclasses import dataclass
from pathlib import Path

from videoxt.utils import ToJsonMixin


@dataclass
class Result(ToJsonMixin):
    """
    A container for the result of an extraction.

    Attributes:
    -----
        `success` (bool | None):
            Whether the extraction was successful.
        `method` (str | None):
            The name of the method that was called.
        `message` (str | None):
            A message describing the result of the extraction.
        `destpath` (Path | None):
            The path to the destination file or directory.
        `elapsed_time` (float | None):
            The number of seconds it took to complete the extraction.

    Methods:
    -----
        - `json()` -> `str`: Return a JSON string representation of the request.
    """

    success: bool | None = None
    method: str | None = None
    message: str | None = None
    destpath: Path | None = None
    elapsed_time: float | None = None
