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
    def parse_create_date(cls, value: int) -> datetime:
        return ConvertDates.unix_to_datetime(value) if isinstance(value, int) else value


class AlertFilterSchema(BaseModel):
    type_alert_name: str | None = None
    station_name: str | None = None
