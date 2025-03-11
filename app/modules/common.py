# -*- coding: utf-8 -*-
from typing import Any


class Singleton(type):
    _instances: dict["Singleton", Any] = {}

    def _call_(cls: "Singleton") -> Any:  # noqa: PLW3201
        if cls not in cls._instances:
            cls.instances[cls] = super(Singleton, cls).call_()  # type: ignore[misc, attr-defined]

        return cls._instances[cls]
