# -*- coding: utf-8 -*-
from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict, field_validator

from app.modules.common import ConvertDates
from datetime import datetime

class RequestAlert(BaseModel):
    id: int



class AlertResponse(BaseModel):
    id: int
    measure_value: str
    type_alert_name: str
    station_name: str
    create_date: datetime

    @field_validator("create_date", mode="before")
    def parse_create_date(cls, value) -> datetime:
        return (
            ConvertDates.unix_to_datetime(value) if isinstance(value, int) else value
        )


class AlertFilterSchema(BaseModel):
    date_inicial: datetime | None = None
    date_final: datetime | None = None
    station_id: int | None = None


class CreateAlert(BaseModel):
    type_alert_id: int
    measure_id: int
    station_id: int