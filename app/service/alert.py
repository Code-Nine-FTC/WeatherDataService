# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.core.models.db_model import Alert
from app.schemas.alert import (
    AlertFilterSchema,
    AlertResponse,
)


class AlertService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def read_alert(self, id_alert: int) -> None:
        await self._session.execute(
            update(Alert).where(Alert.id == id_alert).values(is_read=True)
        )
        await self._session.commit()

    async def get_alerts(self, filters: AlertFilterSchema) -> list[AlertResponse]:
        return await self._buscar_alertas_com_filtros(filters)

    async def _buscar_alertas_com_filtros(
        self, filters: AlertFilterSchema | None = None
    ) -> list[AlertResponse]:
        query_sql = text(
            f"""
            SELECT
                a.id,
                m.value AS measure_value,
                ws."name" AS station_name,
                ta."name" AS type_alert_name,
                to_timestamp(a.create_date) AS create_date
            FROM alerts a
            JOIN measures m
                ON m.id = a.measure_id
            JOIN type_alerts ta
                ON ta.id = a.type_alert_id
            JOIN parameters p
                ON ta.parameter_id = p.id
            JOIN weather_stations ws
                ON ws.id = p.station_id
            WHERE 1=1
            AND ta.is_active = true
            AND a.is_read = false
            {
                "AND ta.name ILIKE :type_alert_name"
                if filters and filters.type_alert_name
                else ""
            }
            {"AND ws.name ILIKE :station_name" if filters and filters.station_name else ""}
            """
        )
        if filters and filters.type_alert_name:
            query_sql = query_sql.bindparams(type_alert_name=f"%{filters.type_alert_name}%")
        if filters and filters.station_name:
            query_sql = query_sql.bindparams(station_name=f"%{filters.station_name}%")

        result = await self._session.execute(query_sql)
        alerts = result.fetchall()
        return [AlertResponse(**alert._asdict()) for alert in alerts]

    async def get_alert_by_id(
        self, alert_id: int
    ) -> AlertResponse:  # Alterado: id_alert -> alert_id
        query = text(
            """
            select
                a.id,
                m.value as measure_value,
                ws."name" as station_name,
                ta."name" as type_alert_name,
                to_timestamp(a.create_date) as create_date
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
        ).bindparams(id_alert=alert_id)
        result = await self._session.execute(query)
        alert = result.fetchone()
        if alert is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta com a ID {alert_id} não encontrado.",
            )
        return AlertResponse(**alert._asdict())
