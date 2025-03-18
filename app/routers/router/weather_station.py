# -*- coding: utf-8 -*-
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.routers.controller.weather_station import WeatherStationController
from app.schemas.weather_station import WeatherStationCreate

router = APIRouter(tags=["Weather Stations"], prefix="/stations")


@router.post("/")
async def create_station(
    data: WeatherStationCreate = Body(...),
    session: AsyncSession = Depends(SessionConnection.session),
) -> None:
    return await WeatherStationController(session, 1).create_station(data, 1)
