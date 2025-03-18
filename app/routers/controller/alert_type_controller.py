# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.alert_type_schema import AlertTypeCreate
from app.service.alert_type_service import AlertTypeService


class AlertTypeController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._service = AlertTypeService(session)

    async def create_alert_type(
        self, alert_type_data: AlertTypeCreate
    ) -> BasicResponse[None]:
        try:
            await self._service.create_alert_type(alert_type_data)
            return BasicResponse[None](data=None)
        except HTTPException as http_ex:
            await self._session.rollback()
            raise http_ex
        except Exception as e:
            await self._session.rollback()
            print(f"Erro ao criar tipo de alerta: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )
