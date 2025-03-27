# -*- coding: utf-8 -*-
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.models.db_model import WeatherStation
from ..schemas.weather_station import WeatherStationCreate, WeatherStationUpdate


class WeatherStationService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _get_station_by_id(self, station_id: int) -> WeatherStation:
        result = await self._session.execute(
            select(WeatherStation).where(WeatherStation.id == station_id)
        )
        station = result.scalar()
        if not station:
            raise HTTPException(status_code=404, detail="Estação não encontrada")
        return station

    async def create_station(self, data: WeatherStationCreate) -> None:
        station_data = data.model_dump()

        if "create_date" in station_data:
            dt = station_data["create_date"]
            if isinstance(dt, datetime):
                station_data["create_date"] = int(dt.timestamp())

        new_station = WeatherStation(**station_data)
        self._session.add(new_station)
        await self._session.commit()

    async def update_station(
        self, station_id: int, data: WeatherStationUpdate
    ) -> None:
        station = await self._get_station_by_id(station_id)

        station_data = data.model_dump()

        for key, value in station_data.items():
            setattr(station, key, value)

        await self._session.commit()

    async def disable_station(self, station_id: int) -> None:
        station = await self._get_station_by_id(station_id)

        station.last_update = datetime.now()  # type: ignore
        station.is_active = False
        await self._session.commit()
