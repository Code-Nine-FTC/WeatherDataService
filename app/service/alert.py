# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.core.models.db_model import Alert
from app.modules.common import ConvertDates
from app.schemas.alert import (
    AlertFilterSchema,
    AlertResponse,
)


class AlertService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def delete_alert(self, id_alert: int) -> None:
        result = await self._session.execute(
            select(Alert).where(Alert.id == id_alert)
        )
        alert = result.scalars().first()
        if alert is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta com a ID {id_alert} não encontrado.",
            )
        await self._session.delete(alert)
        await self._session.commit()

    async def get_alerts(self, filters: AlertFilterSchema) -> list[AlertResponse]:
        return await self._buscar_alertas_com_filtros(filters)

    async def _buscar_alertas_com_filtros(
        self, filters: AlertFilterSchema | None = None
    ) -> list[AlertResponse]:
        query = text(
            f"""
            select
                a.id,
                m.value as measure_value,
                ws."name" as station_name,
                ta."name" as type_alert_name,
                a.create_date
            from alerts a
            join measures m
                on m.id = a.measure_id
            join type_alerts ta
                on ta.id = m.id
            join parameters p
                on ta.parameter_id = p.id
            join weather_stations ws
                on ws.id = p.station_id
            where 1=1
            {
                "and a.create_date >= :date_create"
                if filters and filters.date_inicial
                else ""
            }
            {
                "and a.create_date <= :date_final"
                if filters and filters.date_final
                else ""
            }
            {"and ws.id = :station_id" if filters and filters.station_id else ""}
            """
        )

        if filters.date_inicial:
            query = query.bindparams(
                date_create=ConvertDates.datetime_to_unix(filters.date_inicial)
            )
        if filters.date_final:
            query = query.bindparams(
                date_final=ConvertDates.datetime_to_unix(filters.date_final)
            )
        if filters.station_id:
            query = query.bindparams(station_id=filters.station_id)

        result = await self._session.execute(query)
        alerts = result.fetchall()
        return [AlertResponse(**alert._asdict()) for alert in alerts]

    async def get_alert_by_id(self, id_alert: int) -> AlertResponse:
        query = text(
            """
            select
                a.id,
                m.value as measure_value,
                ws."name" as station_name,
                ta."name" as type_alert_name,
                a.create_date
            from alerts a
            join measures m
                on m.id = a.measure_id
            join type_alerts ta
                on ta.id = m.id
            join parameters p
                on ta.parameter_id = p.id
            join weather_stations ws
                on ws.id = p.station_id
            where 1=1
            and a.id = :id_alert
            """
        ).bindparams(id_alert=id_alert)
        result = await self._session.execute(query)
        alert = result.fetchone()
        if alert is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta com a ID {id_alert} não encontrado.",
            )
        return AlertResponse(**alert._asdict())
