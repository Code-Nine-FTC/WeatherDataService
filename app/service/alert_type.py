# -*- coding: utf-8 -*-


from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.core.models.db_model import Parameter, TypeAlert
from app.schemas.alert_type_schema import (
    AlertTypeCreate,
    AlertTypeResponse,
    AlertTypeUpdate,
)


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

    async def list_alert_types(self, filtros: bool) -> list[AlertTypeResponse]:
        query = select(TypeAlert).where(TypeAlert.is_active == filtros)
        query_result = await self._session.execute(query)
        alert_types = query_result.scalars().all()
        return [
            AlertTypeResponse.model_validate(alert_type, from_attributes=True)
            for alert_type in alert_types
        ]

    async def get_alert_type(self, alert_type_id: int) -> AlertTypeResponse:
        alert_type = await self._session.get(TypeAlert, alert_type_id)
        if alert_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de alerta com a ID {alert_type_id} não encontrado.",
            )
        return AlertTypeResponse.model_validate(alert_type, from_attributes=True)

    async def update_alert_type(
        self, alert_type_id: int, alert_type_data: AlertTypeUpdate
    ) -> None:
        alert_type = await self._search_alert_type_id(alert_type_id)
        data = alert_type_data.model_dump(exclude_unset=True)

        if "name" in data:
            conditions = []
            conditions.append(TypeAlert.name == data.get("name"))
            if "value" in data:
                conditions.append(TypeAlert.value == data.get("value"))
            if "math_signal" in data:
                conditions.append(TypeAlert.math_signal == data.get("math_signal"))
            conditions.append(TypeAlert.id != alert_type.id)
            query_ = select(TypeAlert).where(*conditions)
            query_result = await self._session.execute(query_)
            if query_result.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Tipo de alerta já cadastrado.",
                )

        if data.get("parameter_id") is not None:
            parameter_id = int(data["parameter_id"])
            await self._search_parameter_id(parameter_id)

        await self._session.execute(
            update(TypeAlert).where(TypeAlert.id == alert_type_id).values(**data)
        )

        await self._session.commit()

    async def delete_alert_type(self, alert_type_id: int) -> None:
        await self._search_alert_type_id(alert_type_id)
        await self._session.execute(
            update(TypeAlert)
            .where(TypeAlert.id == alert_type_id)
            .values(is_active=False, last_update=func.now())
        )
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

    async def _search_alert_type_id(self, alert_type_id: int) -> TypeAlert:
        alert_type = await self._session.get(TypeAlert, alert_type_id)
        if alert_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de alerta com a ID {alert_type_id} não encontrado.",
            )
        return alert_type

    async def _search_parameter_id(self, parameter_id: int) -> None:
        parameter = await self._session.get(Parameter, parameter_id)
        if parameter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parâmetro com a ID {parameter_id} não encontrado.",
            )
