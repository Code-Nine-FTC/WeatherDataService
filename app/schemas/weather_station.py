# -*- coding: utf-8 -*-
from datetime import datetime
from app.modules.common import ConvertDates

from pydantic import (
    BaseModel,
    field_validator,
    model_validator,
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
    is_active: bool | None = None
    parameter_types: list[int] | None = None


class FilterWeatherStation(BaseModel):
    uid: str | None = None
    name: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: bool | None = None
    @model_validator(mode="before")
    def parse_dates(cls, value) -> dict:
        if value["start_date"]:
            value["start_date"] = ConvertDates.datetime_to_unix(value["start_date"])
        if value["end_date"]:
            value["end_date"] = ConvertDates.datetime_to_unix(value["end_date"])
        return value


class WeatherStationResponse(BaseModel):
    id: int
    name_station: str
    uid: str
    address: StationAddress
    create_date: datetime
    status: bool

class WeatherStationResponseList(BaseModel):
    id: int
    name: str
    uid: str
    address: StationAddress
    create_date: int
    is_active: bool


