# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.alert import (
    AlertFilterSchema,
    AlertResponse,
    CreateAlert,
)
from app.service.alert import AlertService


class AlertController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._service = AlertService(session)

    async def get_alert_by_id(self, id_alert: int) -> BasicResponse[AlertResponse]:
        try:
            result = await self._service.get_alert_by_id(id_alert)
            return BasicResponse(data=result)
        except HTTPException as http_ex:
            await self._session.rollback()
            raise http_ex
        except Exception as e:
            await self._session.rollback()
            print(f"Erro ao buscar alerta: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )

    async def delete_alert(self, alert_id: int) -> BasicResponse[None]:
        try:
            await self._service.delete_alert(alert_id)
            return BasicResponse(data=None)
        except HTTPException as http_ex:
            await self._session.rollback()
            raise http_ex
        except Exception as e:
            await self._session.rollback()
            print(f"Erro ao deletar alerta: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )

    async def get_filtered_alerts(
        self, filters: AlertFilterSchema
    ) -> BasicResponse[list[AlertResponse]]:
        try:
            alerts = await self._service.get_alerts(filters)
            return BasicResponse(data=alerts)
        except HTTPException as http_ex:
            await self._session.rollback()
            raise http_ex
        except Exception as e:
            await self._session.rollback()
            print(f"Erro ao buscar alertas filtrados: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )

    async def create_alert(self, request: CreateAlert) -> BasicResponse[None]:
        try:
            await self._service.create_alert(request)
            return BasicResponse(data=None)
        except HTTPException as http_ex:
            await self._session.rollback()
            raise http_ex
        except Exception as e:
            await self._session.rollback()
            print(f"Erro ao criar alerta: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )
