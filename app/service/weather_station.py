# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from ..core.models.db_model import WeatherStation
from ..schemas.weather_station import WeatherStationCreate


class WeatherStationService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_station(self, data: WeatherStationCreate) -> None:
        station_data = data.model_dump()

        if "create_date" in station_data:
            dt = station_data["create_date"]
            if isinstance(dt, datetime):
                station_data["create_date"] = int(dt.timestamp())

        new_station = WeatherStation(**station_data)
        self._session.add(new_station)
        await self._session.commit()
