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


@router.patch("/{station_id}")
async def update_station(
    station_id: int,
    data: WeatherStationCreate = Body(...),
    session: AsyncSession = Depends(SessionConnection.session),
) -> dict[str, str]:
    await WeatherStationController(session, 1).update_station(station_id, data)
    return {"detail": "Estação atualizada com sucesso"}


@router.put("/disable/{station_id}")
async def disable_station(
    station_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
) -> dict[str, str]:
    await WeatherStationController(session, 1).disable_station(station_id)
    return {"detail": "Estação desativada com sucesso"}
