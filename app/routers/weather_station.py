# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependency.database import SessionConnection
from app.routers.controller.weather_station import WeatherStationController
from app.schemas.weather_station import WeatherStationCreate, WeatherStationUpdate

router = APIRouter(tags=["Weather Stations"], prefix="/stations")

@router.post("", status_code=201)
async def create_station(
    data: WeatherStationCreate = Body(...),
    session: AsyncSession = Depends(SessionConnection.session),
    #current_user: dict = Depends(get_current_user)
):
    return await WeatherStationController(session).create_station(
        data.model_dump(),
        #current_user.id
    )

