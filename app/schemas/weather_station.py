# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)


class WeatherStationBase(BaseModel):
    name: str
    uid: str
    address: list[str]
    latitude: float
    longitude: float
    create_date: datetime
    is_active: bool

    @field_validator("create_date", mode="before")
    def parse_create_date(cls, value: str | datetime) -> datetime:
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value


class WeatherStationCreate(BaseModel):
    name: str
    uid: str
    latitude: float
    longitude: float


class WeatherStationUpdate(BaseModel):
    name: str | None = None
    uid: str | None = None
    address: list[str] | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool | None = None


class WeatherStationResponse(WeatherStationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
