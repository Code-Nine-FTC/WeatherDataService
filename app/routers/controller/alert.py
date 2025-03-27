# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.alert import RequestAlert
from app.service.alert import AlertService


class AlertController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._service = AlertService(session)

    async def delete_alert(self, requests: RequestAlert) -> BasicResponse[None]:
        try:
            await self._service.delete_alert(requests)
            return BasicResponse[None](data=None)
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
