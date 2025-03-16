# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.alert_type_schema import AlertTypeCreate, AlertTypeResponse
from app.service.alert_type_service import AlertTypeService


class AlertTypeController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._service = AlertTypeService(session)

    async def create_alert_type(
        self, alert_type_data: AlertTypeCreate
    ) -> BasicResponse[AlertTypeResponse]:
        try:
            result = await self._service.create_alert_type(alert_type_data)
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="""Não foi possível criar o tipo de alerta,
                    verifique os dados informados.""",
                )
            return BasicResponse[AlertTypeResponse](data=result)
        except Exception as e:
            print("Erro interno no servidor, tente novamente mais tarde.", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )
