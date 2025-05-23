# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from typing import Any, Dict


class ConvertDates:
    @staticmethod
    def convert(data: Dict[str, Any]) -> Dict[str, Any]:
        date_fields = ["initial_date", "last_data", "last_update"]
        for field in date_fields:
            if field in data and isinstance(data[field], str):
                data[field] = datetime.strptime(data[field], "%Y-%m-%d")
        return data

    @staticmethod
    def unix_to_datetime(unixtime: int) -> datetime | None:
        return (
            datetime.fromtimestamp(unixtime, tz=timezone.utc)
            if isinstance(unixtime, int)
            else None
        )


class Singleton(type):
    _instances: dict["Singleton", Any] = {}

    def __call__(cls: "Singleton", *args: Any, **kwargs: Any) -> Any:  # noqa: PLW3201
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
