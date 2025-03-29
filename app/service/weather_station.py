# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.models.db_model import Parameter, WeatherStation
from ..schemas.weather_station import (
    FilterWeatherStation,
    WeatherStationCreate,
    WeatherStationResponse,
    WeatherStationResponseList,
    WeatherStationUpdate,
)


class WeatherStationService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._parameters: dict[int, Any] = {}

    async def _get_station_by_id(self, station_id: int) -> WeatherStation:
        result = await self._session.execute(
            select(WeatherStation).where(WeatherStation.id == station_id)
        )
        station = result.scalar()
        if not station:
            raise HTTPException(status_code=404, detail="Estação não encontrada")
        return station

    async def _get_parameter(
        self, parameter_id: int, station_id: int
    ) -> Parameter | None:
        query = select(Parameter).where(
            Parameter.parameter_type_id == parameter_id,
            Parameter.station_id == station_id,
        )
        result = await self._session.execute(query)
        parameter = result.scalar()
        return parameter

    async def _create_parameter(
        self, parameter_ids: list[int], station_id: int
    ) -> None:
        for parameter_id in parameter_ids:
            parameter = await self._get_parameter(
                parameter_id=parameter_id, station_id=station_id
            )
            if parameter is None:
                parameter = Parameter(
                    parameter_type_id=parameter_id, station_id=station_id
                )
                self._session.add(parameter)
                await self._session.flush()
        await self._session.commit()

    async def create_station(self, data: WeatherStationCreate) -> None:
        station_data = data.model_dump()
        station = await self._get_station_by_uid(station_data["uid"])
        if station:
            raise HTTPException(
                status_code=400, detail="Estação já existe com este UID."
            )
        parameter_types = station_data.get("parameter_types")
        station_data.pop("parameter_types", None)
        new_station = WeatherStation(**station_data)
        self._session.add(new_station)
        await self._session.flush()
        await self._session.commit()
        if parameter_types and len(parameter_types) > 0:
            await self._create_parameter(parameter_types, new_station.id)

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

    async def get_stations(
        self, filters: FilterWeatherStation
    ) -> list[WeatherStationResponse]:
        query = text(
            f"""
            select ws.id,
                ws."name" as name_station, 
                ws.uid ,
                ws.address,
                ws.create_date,
                ws.is_active as status
            from weather_stations ws 
            where 1=1
            {"and ws.create_date >= :start_date " if filters.start_date else ""}
            {"and ws.create_date <= :end_date" if filters.end_date else ""}   
            {"and ws.uid = :uid " if filters.uid else ""}
            {"and ws.is_active is :status" if filters.status is not None else ""}
            {'and ws."name" is like :name_station ' if filters.name else ""}
            """
        )
        if filters.start_date:
            query = query.bindparams(start_date=filters.start_date)
        if filters.end_date:
            query = query.bindparams(end_date=filters.end_date)
        if filters.uid:
            query = query.bindparams(uid=filters.uid)
        if filters.status is not None:
            query = query.bindparams(status=filters.status)
        if filters.name:
            query = query.bindparams(name_station=f"%{filters.name}%")

        result = await self._session.execute(query)
        stations = result.fetchall()
        return [WeatherStationResponse(**station._asdict()) for station in stations]

    async def get_station_by_id(self, station_id: int) -> WeatherStationResponseList:
        query = select(WeatherStation).where(WeatherStation.id == station_id)
        result = await self._session.execute(query)
        station = result.scalar()
        if not station:
            raise HTTPException(status_code=404, detail="Estação não encontrada")
        return WeatherStationResponseList(**station.__dict__)

    async def _get_station_by_uid(
        self, uid: str
    ) -> WeatherStationResponseList | None:
        query = select(WeatherStation).where(WeatherStation.uid == uid)
        result = await self._session.execute(query)
        station = result.scalar()
        return WeatherStationResponseList(**station.__dict__) if station else None
