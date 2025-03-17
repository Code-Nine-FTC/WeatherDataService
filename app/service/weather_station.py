from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.models.db_model import User, WeatherStation
from ..schemas.weather_station import WeatherStationCreate


class WeatherStationService:
    def __init__(self, session: AsyncSession, user_id: int):
        self._session = session
        self.user = user_id

    async def create_station(self, data: WeatherStationCreate) -> None:
        result = await self._session.execute(
            select(User).where(User.id == self.user)
        )
        if not result.scalar():
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        station_data = data.model_dump()

        if "create_date" in station_data:
            dt = station_data["create_date"]
            if isinstance(dt, datetime):
                station_data["create_date"] = int(dt.timestamp())

        new_station = WeatherStation(**station_data)
        self._session.add(new_station)
        await self._session.commit()
