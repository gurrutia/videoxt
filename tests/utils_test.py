from videoxt.utils import timestamp_to_seconds


def timestamp_to_seconds_test():
    assert timestamp_to_seconds("1") == 1
    assert timestamp_to_seconds("1.1") == 1
    assert timestamp_to_seconds("59") == 59
    assert timestamp_to_seconds("60") == 60
    assert timestamp_to_seconds("0:00") == 0
    assert timestamp_to_seconds("1:01") == 61
    assert timestamp_to_seconds("1:01:01") == 3661
    assert timestamp_to_seconds("1:01:01.1") == 3661
