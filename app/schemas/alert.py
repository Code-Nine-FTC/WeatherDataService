# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel, field_validator

from app.modules.common import ConvertDates


class RequestAlert(BaseModel):
    id: int


class AlertResponse(BaseModel):
    id: int
    measure_value: float
    type_alert_name: str
    station_name: str
    create_date: datetime

    @field_validator("create_date", mode="before")
    def parse_create_date(cls, value: int | datetime) -> datetime:
        if isinstance(value, int):
            dt = ConvertDates.unix_to_datetime(value)
            if dt is None:
                raise ValueError("Invalid unix timestamp for create_date")
            return dt
        if isinstance(value, datetime):
            return value
        raise ValueError("Invalid type for create_date")


class AlertFilterSchema(BaseModel):
    type_alert_name: str | None = None
    station_name: str | None = None
