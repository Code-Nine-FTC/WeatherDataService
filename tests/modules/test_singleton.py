from app.modules.common import Singleton


class MySingleton(metaclass=Singleton):
    pass


def test_singleton_behavior():
    a = MySingleton()
    b = MySingleton()
    assert a is b
