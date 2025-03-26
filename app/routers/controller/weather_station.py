# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.weather_station import WeatherStationCreate, WeatherStationUpdate
from app.service.weather_station import WeatherStationService


class WeatherStationController:
    def __init__(self, session: AsyncSession, user_id: int) -> None:
        self._session = session
        self._user_id = user_id
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

    async def update_station(
        self, station_id: int, data: WeatherStationUpdate
    ) -> BasicResponse[None]:
        try:
            await self._service.update_station(station_id, data)
            return BasicResponse[None](data=None)
        except HTTPException as e:
            if e.status_code in {400, 403, 404}:
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}",
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Parâmetros inválidos: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}",
            )

    async def disable_station(self, station_id: int) -> BasicResponse[None]:
        try:
            await self._service.disable_station(station_id)
            return BasicResponse[None](data=None)
        except HTTPException as e:
            if e.status_code in {400, 403, 404}:
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}",
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Parâmetros inválidos: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}",
            )
