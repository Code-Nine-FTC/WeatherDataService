# -*- coding: utf-8 -*-

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from fastapi import HTTPException, status

from app.core.models.db_model import TypeAlert, Parameter
from app.schemas.alert_type_schema import AlertTypeCreate


class AlertTypeService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_alert_type(self, alert_type_date: AlertTypeCreate) -> None:
        # precisa verificar se o tipo de alerta já existe e o parameto_id
        
        alert_type_dict = alert_type_date.model_dump() # trasnforma em um dicionário
        parameter_id = alert_type_dict.pop("parameter_id", None) # tira o parametro_id para 
        new_alert_type = TypeAlert(**alert_type_dict) # não dar erro caso seja nulo

        query = select(TypeAlert).where(
            TypeAlert.name == new_alert_type.name,
            TypeAlert.value == new_alert_type.value,
            TypeAlert.math_signal == new_alert_type.math_signal
        )
        
        query_result = await self._session.execute(query)
        if (query_result.fetchone()):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tipo de alerta com mesmo nome, valor e sinal matemático já existe."
            )
        
        if parameter_id is not None:
            parameter = await self._session.get(Parameter, parameter_id)
            if parameter is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parâmetro com a ID {parameter_id} não encontrado.")
            new_alert_type.parameter_id = parameter_id #se não for nulo é adicionado de volta para cadastrar

        self._session.add(new_alert_type)
        await self._session.commit()

    # async def _exemple(self) -> None:
    #     query_result = await self._session.execute(text("SELECT 1 "))
    #     row_result = query_result.fetchone()
    #     result_dict = {"value": str(row_result)}
    #     self._result = ResponseExempleService(**result_dict) if row_result else None
