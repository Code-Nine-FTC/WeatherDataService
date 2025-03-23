# -*- coding: utf-8 -*-

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_model import Parameter, TypeAlert
from app.schemas.alert_type_schema import AlertTypeCreate


class AlertTypeService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_alert_type(self, alert_type_date: AlertTypeCreate) -> None:
        if alert_type_date.parameter_id is not None:
            await self._search_parameter_id(alert_type_date.parameter_id)

        new_alert_type = TypeAlert(**alert_type_date.model_dump())

        await self._search_alert_type(new_alert_type)

        self._session.add(new_alert_type)
        await self._session.commit()

    async def _search_alert_type(self, new_alert_type: TypeAlert) -> None:
        query = select(TypeAlert).where(
            TypeAlert.name == new_alert_type.name,
            TypeAlert.value == new_alert_type.value,
            TypeAlert.math_signal == new_alert_type.math_signal,
        )

        query_result = await self._session.execute(query)

        if query_result.fetchone():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tipo de alerta já cadastrado.",
            )

    async def _search_parameter_id(self, parameter_id: int) -> None:
        parameter = await self._session.get(Parameter, parameter_id)
        if parameter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parâmetro com a ID {parameter_id} não encontrado.",
            )
