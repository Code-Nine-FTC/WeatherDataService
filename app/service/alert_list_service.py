from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.models.db_model import Alert, Measure, TypeAlert, WeatherStation
from app.modules.common import ConvertDates
from app.schemas.alert_list_schema import AlertFilterSchema, AlertResponse


class AlertListService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_alerts(self) -> List[AlertResponse]:
        return await self._buscar_alertas_com_filtros()

    async def get_filtered_alerts(
        self, filters: AlertFilterSchema
    ) -> List[AlertResponse]:
        return await self._buscar_alertas_com_filtros(filters)

    async def _buscar_alertas_com_filtros(
        self, filters: Optional[AlertFilterSchema] = None
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

        return [
            AlertResponse.model_validate({
                "id": alert.id,
                "measure_value": alert.measure.value,
                "type_alert_name": alert.type_alert.name,
                "station_name": alert.type_alert.parameter.station_id,
                "create_date": alert.create_date,
            })
            for alert in alerts
        ]
