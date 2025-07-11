from datetime import datetime

from app.modules.common import ConvertDates, Singleton


def test_unix_to_datetime() -> None:
    result = ConvertDates.unix_to_datetime(1712553600)
    assert isinstance(result, datetime)


class MySingleton(metaclass=Singleton):
    pass


def test_singleton_instance() -> None:
    a = MySingleton()
    b = MySingleton()
    assert a is b
