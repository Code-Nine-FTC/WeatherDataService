# -*- coding: utf-8 -*-
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.models.db_model import Parameter, WeatherStation
from ..schemas.weather_station import WeatherStationCreate, WeatherStationUpdate


class WeatherStationService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._parameters = {}

    async def _get_station_by_id(self, station_id: int) -> WeatherStation:
        result = await self._session.execute(
            select(WeatherStation).where(WeatherStation.id == station_id)
        )
        station = result.scalar()
        if not station:
            raise HTTPException(status_code=404, detail="Estação não encontrada")
        return station

    async def _get_parameter(self, parameter_id: int, station_id: int) -> None:
        query = select(WeatherStation).where(
            WeatherStation.id == station_id,
            WeatherStation.parameter_id == parameter_id,
        )
        result = await self._session.execute(query)
        parameter = result.scalar()
        if not parameter:
            raise HTTPException(status_code=404, detail="Parâmetro não encontrado")
        return parameter

    async def _create_parameter(
        self, parameter_ids: list[int], station_id: int
    ) -> None:
        for parameter_id in parameter_ids:
            parameter = await self._get_parameter(
                parameter_id=parameter_id, station_id=station_id
            )
            if parameter is None:
                parameter = Parameter(id=parameter_id, station_id=station_id)
                self._session.add(parameter)
                await self._session.flush()
        await self._session.commit()

    async def create_station(self, data: WeatherStationCreate) -> None:
        station_data = data.model_dump()
        parameter_types = station_data.get("parameter_types")
        station_data.pop("parameter_types", None)
        new_station = WeatherStation(**station_data)
        self._session.add(new_station)
        await self._session.flush()
        if parameter_types or len(parameter_types) > 0:
            await self._create_parameter(parameter_types, new_station.id)
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
