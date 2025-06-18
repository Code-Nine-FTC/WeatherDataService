# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.models.db_model import Parameter, WeatherStation
from ..schemas.weather_station import (
    FilterWeatherStation,
    PameterByStation,
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

    async def _get_parameter(self, parameter_id: int, station_id: int) -> Parameter | None:
        query = select(Parameter).where(
            Parameter.parameter_type_id == parameter_id,
            Parameter.station_id == station_id,
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def _create_parameter(self, parameter_ids: list[int], station_id: int) -> None:
        existing_query = select(Parameter).where(Parameter.station_id == station_id)
        result = await self._session.execute(existing_query)
        existing_parameters = result.scalars().all()

        existing_params_map = {param.parameter_type_id: param for param in existing_parameters}
        new_ids = set(parameter_ids)

        # Remover parâmetros que não estão na nova lista
        for existing_type_id, param_obj in existing_params_map.items():
            if existing_type_id not in new_ids and param_obj.is_active:
                param_obj.is_active = False
                self._session.add(param_obj)

        for desired_type_id in new_ids:
            if desired_type_id in existing_params_map:
                param_obj = existing_params_map[desired_type_id]
                if not param_obj.is_active:
                    param_obj.is_active = True
                    self._session.add(param_obj)
            else:
                new_parameter = Parameter(
                    parameter_type_id=desired_type_id, station_id=station_id
                )
                self._session.add(new_parameter)

        await self._session.flush()
        await self._session.commit()

    async def create_station(self, data: WeatherStationCreate) -> None:
        station_data = data.model_dump()
        station = await self._get_station_by_uid(station_data["uid"])
        if station:
            raise HTTPException(status_code=400, detail="Estação já existe com este UID.")
        parameter_types = station_data.get("parameter_types")
        station_data.pop("parameter_types", None)
        new_station = WeatherStation(**station_data)
        self._session.add(new_station)
        await self._session.flush()
        await self._session.commit()
        if parameter_types and len(parameter_types) > 0:
            await self._create_parameter(parameter_types, new_station.id)

    async def update_station(self, station_id: int, data: WeatherStationUpdate) -> None:
        station = await self._get_station_by_id(station_id)
        station_data = data.model_dump(exclude_unset=True)

        if "parameter_types" in station_data:
            parameter_ids = station_data["parameter_types"]
            if isinstance(parameter_ids, list):
                await self._create_parameter(parameter_ids, station_id)
            station_data.pop("parameter_types", None)

        if "address" in station_data:
            current_address = station.address if isinstance(station.address, dict) else {}
            updated_address = station_data.pop("address")
            current_address.update(updated_address)
            station_data["address"] = current_address

        if station_data:
            await self._session.execute(
                update(WeatherStation)
                .where(WeatherStation.id == station_id)
                .values(**station_data)
            )

        await self._session.commit()

    async def disable_station(self, station_id: int) -> None:
        station = await self._get_station_by_id(station_id)

        station.last_update = datetime.now()  # type: ignore
        station.is_active = not station.is_active
        await self._session.commit()

    async def get_stations(
        self, filters: FilterWeatherStation
    ) -> list[WeatherStationResponse]:
        query = text(
            f"""
            SELECT
                ws.id,
                ws."name" AS name_station,
                ws.uid,
                ws.address,
                ws.latitude,
                ws.longitude,
                ws.create_date,
                ws.is_active,
                COALESCE(
                (SELECT JSONB_AGG(
                    JSONB_BUILD_OBJECT(
                        'parameter_id', p.id,
                        'parameter_type_id', p.parameter_type_id,
                        'name_parameter', pt.name
                    )
                )
                FROM parameters p
                join parameter_types pt
                on pt.id = p.parameter_type_id
                WHERE p.station_id::BIGINT = ws.id
                AND p.is_active = true),
                '[]'::JSONB
            ) AS parameters
            FROM weather_stations ws
            where 1 = 1
            {"and ws.uid = :uid " if filters.uid is not None else ""}
            {"and ws.is_active = :is_active" if filters.is_active is not None else ""}
            {'and ws."name" like :name_station ' if filters.name is not None else ""}
            """
        )
        if filters.uid:
            query = query.bindparams(uid=filters.uid)
        if filters.is_active is not None:
            query = query.bindparams(is_active=filters.is_active)
        if filters.name:
            query = query.bindparams(name_station=f"%{filters.name}%")

        result = await self._session.execute(query)
        stations = result.fetchall()
        return [WeatherStationResponse(**station._asdict()) for station in stations]

    async def get_station_by_id(self, station_id: int) -> WeatherStationResponseList:
        query = text(
            """
            SELECT
                ws.id,
                ws."name",
                ws.uid,
                ws.address,
                ws.latitude,
                ws.longitude,
                ws.create_date,
                ws.is_active,
                COALESCE(
                (SELECT JSONB_AGG(
                    JSONB_BUILD_OBJECT(
                        'parameter_id', p.id,
                        'parameter_type_id', p.parameter_type_id,
                        'name_parameter', pt.name
                    )
                )
                FROM parameters p
                join parameter_types pt
                on pt.id = p.parameter_type_id
                WHERE p.station_id::BIGINT = ws.id
                AND p.is_active = true),
                '[]'::JSONB
            ) AS parameters
            FROM weather_stations ws
            where 1 = 1
            and ws.id = :station_id
            """
        ).bindparams(station_id=station_id)
        result = await self._session.execute(query)
        station = result.fetchone()
        if not station:
            raise HTTPException(status_code=404, detail="Estação não encontrada")
        return WeatherStationResponseList(**station._asdict())

    async def _get_station_by_uid(self, uid: str) -> WeatherStationResponseList | None:
        query = select(WeatherStation).where(WeatherStation.uid == uid)
        result = await self._session.execute(query)
        station = result.scalar()
        weatherstation = station.__dict__ if station else None
        if weatherstation:
            weatherstation.pop("_sa_instance_state", None)
        return WeatherStationResponseList(**weatherstation) if weatherstation else None

    async def get_station_by_parameter(self, parmater_type_id: int) -> list[PameterByStation]:
        query = text(
            """
            select
                p.id,
                ws.name
            from weather_stations ws
            join parameters p
                on ws.id = p.station_id
            join parameter_types pt
                on p.parameter_type_id = pt.id
            where pt.id = :parameter_type_id
            and ws.is_active = true
            """
        ).bindparams(parameter_type_id=parmater_type_id)
        result = await self._session.execute(query)
        station = result.fetchall()
        return [PameterByStation(**station._asdict()) for station in station]
