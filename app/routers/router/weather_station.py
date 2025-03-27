# -*- coding: utf-8 -*-
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.auth import AuthManager
from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.weather_station import WeatherStationController
from app.schemas.user import UserResponse
from app.schemas.weather_station import WeatherStationCreate, WeatherStationUpdate

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
    return await WeatherStationController(session, current_user.id).create_station(
        data
    )


@router.patch("/{station_id}")
async def update_station(
    station_id: int,
    data: WeatherStationUpdate = Body(...),
    session: AsyncSession = Depends(SessionConnection.session),
    current_user: UserResponse = Depends(AuthManager.has_authorization),
) -> BasicResponse[None]:
    return await WeatherStationController(session, current_user.id).update_station(
        station_id, data
    )


@router.patch("/disable/{station_id}")
async def disable_station(
    station_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
    current_user: UserResponse = Depends(AuthManager.has_authorization),
) -> BasicResponse[None]:
    return await WeatherStationController(session, current_user.id).disable_station(
        station_id
    )
