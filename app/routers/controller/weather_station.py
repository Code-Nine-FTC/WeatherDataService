# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError  # ✅ Import necessário para tratar conflito
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.weather_station import (
    FilterWeatherStation,
    PameterByStation,
    WeatherStationCreate,
    WeatherStationResponse,
    WeatherStationResponseList,
    WeatherStationUpdate,
)
from app.service.weather_station import WeatherStationService


class WeatherStationController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._service = WeatherStationService(session)

    async def create_station(self, data: WeatherStationCreate) -> BasicResponse[None]:
        try:
            await self._service.create_station(data)
            return BasicResponse(data=None)
        except IntegrityError:
            await self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma estação com esse UID.",
            )
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
            return BasicResponse(data=None)
        except HTTPException as e:
            raise e
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

    async def get_stations_by_id(
        self, station_id: int
    ) -> BasicResponse[WeatherStationResponseList]:
        try:
            stations = await self._service.get_station_by_id(station_id)
            return BasicResponse(data=stations)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}",
            )

    async def get_stations_by_filters(
        self, filters: FilterWeatherStation
    ) -> BasicResponse[list[WeatherStationResponse]]:
        try:
            stations = await self._service.get_stations(filters)
            return BasicResponse(data=stations)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}",
            )

    async def get_parameter_by_station(
        self, type_parameter_id: int
    ) -> BasicResponse[list[PameterByStation]]:
        try:
            stations = await self._service.get_station_by_parameter(type_parameter_id)
            return BasicResponse(data=stations)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(e)}",
            )
