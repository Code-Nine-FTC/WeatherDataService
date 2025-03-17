# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.basic_response import BasicResponse
from app.schemas.weather_station import WeatherStationResponse
from app.service.weather_station import WeatherStationService

class WeatherStationController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._service = WeatherStationService(session)
        self._result: WeatherStationResponse | None = None

    async def create_station(self, data: dict, user_id: int) -> BasicResponse[WeatherStationResponse]:
        try:
            async with self._session.begin():
                self._result = await self._service.create_station(data, user_id)
                return BasicResponse[WeatherStationResponse](data=self._result)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}"
            )

    