# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import (
    BaseModel,
    field_validator,
)

from app.modules.common import ConvertDates


class StationAddress(BaseModel):
    city: str
    state: str
    country: str


class WeatherStationBase(BaseModel):
    name: str
    uid: str
    address: StationAddress
    latitude: float
    longitude: float
    create_date: datetime
    is_active: bool

    @field_validator("create_date", mode="before")
    def parse_create_date(cls, value: str | datetime) -> datetime:
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value


class StationAdressUpdate(BaseModel):
    city: str | None = None
    state: str | None = None
    country: str | None = None


class WeatherStationCreate(BaseModel):
    name: str
    uid: str
    latitude: float
    longitude: float
    address: StationAddress
    description: str | None = None
    parameter_types: list[int] = []


class WeatherStationUpdate(BaseModel):
    name: str | None = None
    uid: str | None = None
    address: StationAdressUpdate | None = None
    latitude: float | None = None
    longitude: float | None = None
    description: str | None = None
    last_update: datetime | None = None
    is_active: bool | None = None
    parameter_types: list[int] | None = None


class FilterWeatherStation(BaseModel):
    uid: str | None = None
    name: str | None = None
    is_active: bool | None = None


class WeatherStationResponse(BaseModel):
    id: int
    name_station: str
    uid: str
    address: StationAddress | None = None
    latitude: float
    longitude: float
    description: str | None = None
    create_date: datetime
    is_active: bool
    parameters: list[dict[str, Any]] | None = []

    @field_validator("create_date", mode="before")
    def parse_create_date(cls, value: int) -> datetime:
        if value is None:
            raise ValueError("create_date cannot be None")
        dt = ConvertDates.unix_to_datetime(value)
        if dt is None:
            raise ValueError("Invalid unix timestamp for create_date")
        return dt


class WeatherStationResponseList(BaseModel):
    id: int
    name: str
    uid: str
    address: StationAddress | None = None
    latitude: float
    longitude: float
    description: str | None = None
    create_date: int
    is_active: bool
    parameters: list[dict[str, Any]] | None = []


class PameterByStation(BaseModel):
    id: int
    name_station: str
