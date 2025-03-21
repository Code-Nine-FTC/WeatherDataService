from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.modules.common import ConvertDates


class AlertBase(BaseModel):
    measure_value: str
    type_alert_name: str
    station_name: str
    create_date: datetime

    @field_validator("create_date", mode="before")
    def parse_create_date(cls, value: int | datetime) -> datetime:
        return (
            ConvertDates.unix_to_datetime(value) if isinstance(value, int) else value
        )

class AlertResponse(AlertBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
