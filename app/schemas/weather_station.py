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


class StationAddress(BaseModel):
    city: str
    state: str
    country: str


class WeatherStationCreate(BaseModel):
    name: str
    uid: str
    latitude: float
    longitude: float
    address: StationAddress
    parameter_types: list[int] = []


class WeatherStationUpdate(BaseModel):
    name: str | None = None
    uid: str | None = None
    address: list[str] | None = None
    latitude: float | None = None
    longitude: float | None = None
    last_update: datetime = datetime.now()


class WeatherStationResponse(WeatherStationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class FilterWeatherStation(BaseModel):
    uid: str = None
    name: str = None
    start_date: datetime = None
    end_date: datetime = None
    status: bool = None


class WeatherStationResponse(BaseModel):
    id: int
    name_station: str
    uid: str
    address: list[str]
    create_date: datetime
    status: bool
