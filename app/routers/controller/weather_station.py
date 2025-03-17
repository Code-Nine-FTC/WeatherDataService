# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.weather_station import WeatherStationCreate
from app.service.weather_station import WeatherStationService


class WeatherStationController:
    def __init__(self, session: AsyncSession, user_id: int) -> None:
        self._session = session
        self._service = WeatherStationService(session, user_id)

    async def create_station(
        self, data: WeatherStationCreate, user_id: int
    ) -> None:
        try:
            async with self._session.begin():
                await self._service.create_station(data)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}",
            )
