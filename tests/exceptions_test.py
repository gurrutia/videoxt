import pytest

from videoxt.exceptions import ValidationException


def test_validation_exception():
    with pytest.raises(ValidationException) as exc_info:
        raise ValidationException("Custom error message")

    assert str(exc_info.value) == "Custom error message"
