from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, ConfigDict

from app.modules.common import ConvertDates


class AlertBase(BaseModel):
    measure_value: str
    type_alert_name: str
    station_name: str
    create_date: datetime

    @field_validator("create_date", mode="before")
    def parse_create_date(cls, value) -> datetime:
        return ConvertDates.unix_to_datetime(value) if isinstance(value, int) else value


class AlertResponse(AlertBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AlertFilterSchema(BaseModel):
    date_inicial: Optional[datetime] = None
    date_final: Optional[datetime] = None
    station_id: Optional[int] = None
