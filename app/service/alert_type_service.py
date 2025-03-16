# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.core.models.db_model import TypeAlert
from app.schemas.alert_type_schema import AlertTypeCreate, AlertTypeResponse
from app.schemas.exemple import ResponseExempleService


class AlertTypeService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_alert_type(
        self, alert_type_date: AlertTypeCreate
    ) -> AlertTypeResponse:
        now = int(datetime.utcnow().timestamp())

        new_alert_type = TypeAlert(
            name=alert_type_date.name,
            value=alert_type_date.value,
            math_signal=alert_type_date.math_signal,
            create_date=now,
            last_update=now,
            status=alert_type_date.status,
        )

        self._session.add(new_alert_type)
        await self._session.commit()
        await self._session.refresh(new_alert_type)

        return AlertTypeResponse(
            id=new_alert_type.id,
            name=new_alert_type.name,
            value=new_alert_type.value,
            math_signal=new_alert_type.math_sign,
            create_date=new_alert_type.initial_date,
            last_update=new_alert_type.last_update,
            status=new_alert_type.status,
        )

    async def _exemple(self) -> None:
        query_result = await self._session.execute(text("SELECT 1 "))
        row_result = query_result.fetchone()
        result_dict = {"value": str(row_result)}
        self._result = ResponseExempleService(**result_dict) if row_result else None
