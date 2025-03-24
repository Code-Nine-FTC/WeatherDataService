# -*- coding: utf-8 -*-
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.auth import AuthManager
from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.weather_station import WeatherStationController
from app.schemas.weather_station import WeatherStationCreate

router = APIRouter(
    tags=["Weather Stations"],
    prefix="/stations",
    dependencies=[Depends(AuthManager.has_authorization)],
)

@router.post("/")
async def create_station(
    session: AsyncSession = Depends(SessionConnection.session),
    data: WeatherStationCreate = Body(...),
) -> BasicResponse[None]:
    return await WeatherStationController(session).create_station(data)
