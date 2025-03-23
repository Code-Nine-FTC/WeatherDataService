# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.weather_station import WeatherStationCreate
from app.service.weather_station import WeatherStationService


class WeatherStationController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._service = WeatherStationService(session)

    async def create_station(
        self, data: WeatherStationCreate
    ) -> BasicResponse[None]:
        try:
            await self._service.create_station(data)
            return BasicResponse[None](data=None)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}",
            )
