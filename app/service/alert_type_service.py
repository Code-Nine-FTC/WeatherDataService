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
    ) -> None:
        new_alert_type = TypeAlert(**alert_type_date.model_dump())
        self._session.add(new_alert_type)
        await self._session.commit()
    
    async def _exemple(self) -> None:
        query_result = await self._session.execute(text("SELECT 1 "))
        row_result = query_result.fetchone()
        result_dict = {"value": str(row_result)}
        self._result = ResponseExempleService(**result_dict) if row_result else None
