# -*- coding: utf-8 -*-
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.auth import AuthManager
from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.weather_station import WeatherStationController
from app.schemas.user import UserResponse
from app.schemas.weather_station import WeatherStationCreate, WeatherStationResponse, WeatherStationResponseList, WeatherStationUpdate

router = APIRouter(
    tags=["Weather Stations"],
    prefix="/stations",
    dependencies=[Depends(AuthManager.has_authorization)],
)


@router.post("/")
async def create_station(
    session: AsyncSession = Depends(SessionConnection.session),
    data: WeatherStationCreate = Body(...),
    current_user: UserResponse = Depends(AuthManager.has_authorization),
) -> BasicResponse[None]:
    return await WeatherStationController(session).create_station(
        data
    )


@router.get("/filters")
async def get_filtered_stations(
    filters: dict = Body(...),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[WeatherStationResponse]:
    return await WeatherStationController(session).get_stations_by_filters(filters)


@router.get("/{station_id}")
async def get_station_by_id(
    station_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[WeatherStationResponseList]:
    return await WeatherStationController(session).get_stations_by_id(station_id)


@router.patch("/{station_id}")
async def update_station(
    station_id: int,
    data: WeatherStationUpdate = Body(...),
    session: AsyncSession = Depends(SessionConnection.session),
    current_user: UserResponse = Depends(AuthManager.has_authorization),
) -> BasicResponse[None]:
    return await WeatherStationController(session).update_station(
        station_id, data
    )


@router.patch("/disable/{station_id}")
async def disable_station(
    station_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
    current_user: UserResponse = Depends(AuthManager.has_authorization),
) -> BasicResponse[None]:
    return await WeatherStationController(session).disable_station(
        station_id
    )
