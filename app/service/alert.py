# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.models.db_model import Alert, Measures, TypeAlert, WeatherStation
from app.modules.common import ConvertDates
from app.schemas.alert import (
    AlertFilterSchema,
    AlertResponse,
    CreateAlert,
    RequestAlert,
)


class AlertService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def delete_alert(self, id_alert: RequestAlert) -> None:
        result = await self._session.execute(
            select(Alert).where(Alert.id == id_alert.id)
        )
        alert = result.scalars().first()
        if alert is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta com a ID {id_alert.id} não encontrado.",
            )
        await self._session.delete(alert)
        await self._session.commit()

    async def get_alerts(self) -> list[AlertResponse]:
        return await self._buscar_alertas_com_filtros()

    async def get_filtered_alerts(
        self, filters: AlertFilterSchema
    ) -> list[AlertResponse]:
        return await self._buscar_alertas_com_filtros(filters)

    async def _buscar_alertas_com_filtros(
        self, filters: AlertFilterSchema | None = None
    ) -> list[AlertResponse]:
        query = (
            select(Alert)
            .join(Measures, Alert.measure_id == Measures.id)
            .join(TypeAlert, Alert.type_alert_id == TypeAlert.id)
            .join(WeatherStation, TypeAlert.parameter_id == WeatherStation.id)
            .options(
                joinedload(Alert.measure),
                joinedload(Alert.type_alert),
                joinedload(TypeAlert.parameter),
            )
        )

        if filters:
            if filters.date_inicial:
                query = query.where(
                    Alert.create_date
                    >= ConvertDates.datetime_to_unix(filters.date_inicial)
                )
            if filters.date_final:
                query = query.where(
                    Alert.create_date
                    <= ConvertDates.datetime_to_unix(filters.date_final)
                )
            if filters.station_id is not None:
                query = query.where(WeatherStation.id == filters.station_id)

        result = await self._session.execute(query)
        alerts = result.scalars().all()

        return [AlertResponse(**dict(alert)) for alert in alerts]

    async def get_alert_by_id(self, id_alert: RequestAlert) -> AlertResponse:
        result = await self._session.execute(
            select(Alert).where(Alert.id == id_alert.id)
        )
        alert = result.scalars().first()
        if alert is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta com a ID {id_alert.id} não encontrado.",
            )
        return AlertResponse(**dict(alert))

    async def create_alert(self, alert_data: CreateAlert) -> None:
        alert = Alert(**alert_data.model_dump())
        self._session.add(alert)
        await self._session.flush()
        await self._session.commit()
