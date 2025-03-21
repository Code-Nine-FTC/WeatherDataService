from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.models.db_model import Alert, Measure, TypeAlert, WeatherStation
from app.modules.common import ConvertDates
from app.schemas.alert_schema import AlertResponse


class AlertListService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_alerts(self) -> List[AlertResponse]:
        query = (
            select(Alert)
            .join(Measure, Alert.measure_id == Measure.id)
            .join(TypeAlert, Alert.type_alert_id == TypeAlert.id)
            .join(WeatherStation, TypeAlert.parameter_id == WeatherStation.id)
            .options(
                joinedload(Alert.measure),
                joinedload(Alert.type_alert),
                joinedload(TypeAlert.parameter),
            )
        )

        query_result = await self._session.execute(query)
        alerts = query_result.scalars().all()

        if not alerts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum alerta encontrado.",
            )

        return [
            AlertResponse(
                id=alert.id,
                measure_value=alert.measure.value,
                type_alert_name=alert.type_alert.name,
                station_name=alert.type_alert.parameter.station_id,
                create_date=ConvertDates.unix_to_datetime(alert.create_date),
            )
            for alert in alerts
        ]

    async def get_filtered_alerts(
        self,
        date_inicial: Optional[datetime] = None,
        date_final: Optional[datetime] = None,
        station_id: Optional[int] = None,
    ) -> List[AlertResponse]:
        query = (
            select(Alert)
            .join(Measure, Alert.measure_id == Measure.id)
            .join(TypeAlert, Alert.type_alert_id == TypeAlert.id)
            .join(WeatherStation, TypeAlert.parameter_id == WeatherStation.id)
            .options(
                joinedload(Alert.measure),
                joinedload(Alert.type_alert),
                joinedload(TypeAlert.parameter),
            )
        )

        if date_inicial:
            query = query.where(Alert.create_date >= ConvertDates.datetime_to_unix(date_inicial))
        if date_final:
            query = query.where(Alert.create_date <= ConvertDates.datetime_to_unix(date_final))
        if station_id is not None:
            query = query.where(WeatherStation.id == station_id)

        query_result = await self._session.execute(query)
        alerts = query_result.scalars().all()

        if not alerts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum alerta encontrado com os filtros fornecidos.",
            )

        return [
            AlertResponse(
                id=alert.id,
                measure_value=alert.measure.value,
                type_alert_name=alert.type_alert.name,
                station_name=alert.type_alert.parameter.station_id,
                create_date=ConvertDates.unix_to_datetime(alert.create_date),
            )
            for alert in alerts
        ]
