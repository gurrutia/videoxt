from dataclasses import dataclass
from typing import Optional

from videoxt.utils import ToJsonMixin


@dataclass
class Result(ToJsonMixin):
    """
    A container for the result of an extraction.

    Attributes:
    -----
        `success` (bool):
            Whether the extraction was successful.
        `method` (str):
            The name of the method that was called.
        `message` (str):
            A message describing the result of the extraction.
        `destpath` (str):
            The path to the destination file or directory.
        `elapsed_time` (float):
            The number of seconds it took to complete the extraction.

    Methods:
    -----
        - `json()` -> `str`: Return a JSON string representation of the request.
    """

    success: Optional[bool] = None
    method: Optional[str] = None
    message: Optional[str] = None
    destpath: Optional[str] = None
    elapsed_time: Optional[float] = None

    def __str__(self) -> str:
        return f"[yellow]<Result>[/yellow]\n{self.json()}"
