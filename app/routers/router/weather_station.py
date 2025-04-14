# -*- coding: utf-8 -*-
from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.auth import AuthManager
from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.weather_station import WeatherStationController
from app.schemas.user import UserResponse
from app.schemas.weather_station import (
    FilterWeatherStation,
    PameterByStation,
    WeatherStationCreate,
    WeatherStationResponse,
    WeatherStationResponseList,
    WeatherStationUpdate,
)

router = APIRouter(
    tags=["Weather Stations"],
    prefix="/stations",
)


@router.post("/", dependencies=[Depends(AuthManager.has_authorization)])
async def create_station(
    session: AsyncSession = Depends(SessionConnection.session),
    data: WeatherStationCreate = Body(...),
    current_user: UserResponse = Depends(AuthManager.has_authorization),
) -> BasicResponse[None]:
    return await WeatherStationController(session).create_station(data)


@router.get("/filters")
async def get_filtered_stations(
    filters: FilterWeatherStation = Query(),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[WeatherStationResponse]]:
    return await WeatherStationController(session).get_stations_by_filters(filters)


@router.get("/parameters/{type_parameter_id}")
async def get_parameters_by_station(
    type_paramter_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[PameterByStation]]:
    return await WeatherStationController(session).get_parameter_by_station(type_paramter_id)


@router.get("/{station_id}")
async def get_station_by_id(
    station_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[WeatherStationResponseList]:
    return await WeatherStationController(session).get_stations_by_id(station_id)


@router.patch("/{station_id}", dependencies=[Depends(AuthManager.has_authorization)])
async def update_station(
    station_id: int,
    data: WeatherStationUpdate = Body(...),
    session: AsyncSession = Depends(SessionConnection.session),
    current_user: UserResponse = Depends(AuthManager.has_authorization),
) -> BasicResponse[None]:
    return await WeatherStationController(session).update_station(station_id, data)


@router.patch("/disable/{station_id}", dependencies=[Depends(AuthManager.has_authorization)])
async def disable_station(
    station_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
    current_user: UserResponse = Depends(AuthManager.has_authorization),
) -> BasicResponse[None]:
    return await WeatherStationController(session).disable_station(station_id)
