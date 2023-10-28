"""Containers for extraction results."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from videoxt.utils import ToJsonMixin


@dataclass
class Result(ToJsonMixin):
    """
    A container for the result of an extraction.

    Attributes:
    -----
        `success` (Optional[bool]):
            Whether the extraction was successful.
        `method` (Optional[str]):
            The name of the method that was called.
        `message` (Optional[str]):
            A message describing the result of the extraction.
        `destpath` (Optional[Path]):
            The path to the destination file or directory.
        `elapsed_time` (Optional[float]):
            The number of seconds it took to complete the extraction.

    Methods:
    -----
        - `json()` -> `str`: Return a JSON string representation of the request.
    """

    success: Optional[bool] = None
    method: Optional[str] = None
    message: Optional[str] = None
    destpath: Optional[Path] = None
    elapsed_time: Optional[float] = None
