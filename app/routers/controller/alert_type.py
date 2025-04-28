# -*- coding: utf-8 -*-

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.alert_type_schema import (
    AlertTypeCreate,
    AlertTypeResponse,
    AlertTypeUpdate,
)
from app.service.alert_type import AlertTypeService


class AlertTypeController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._service = AlertTypeService(session)

    async def create_alert_type(self, alert_type_data: AlertTypeCreate) -> BasicResponse[None]:
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

    async def list_alert_types(self, filters: bool) -> BasicResponse[list[AlertTypeResponse]]:
        try:
            alert_types = await self._service.list_alert_types(filters)
            return BasicResponse[list[AlertTypeResponse]](data=alert_types)
        except Exception as http_ex:
            raise http_ex
        except Exception as e:
            print(f"Erro ao listar tipos de alerta: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )

    async def get_alert_type(self, alert_type_id: int) -> BasicResponse[AlertTypeResponse]:
        try:
            alert_type = await self._service.get_alert_type(alert_type_id)
            return BasicResponse[AlertTypeResponse](data=alert_type)
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            print(f"Erro ao buscar tipo de alerta: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )

    async def update_alert_type(
        self, alert_type_id: int, alert_type_data: AlertTypeUpdate
    ) -> BasicResponse[None]:
        try:
            await self._service.update_alert_type(alert_type_id, alert_type_data)
            return BasicResponse[None](data=None)
        except HTTPException as http_ex:
            await self._session.rollback()
            raise http_ex
        except Exception as e:
            await self._session.rollback()
            print(f"Erro ao atualizar tipo de alerta: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )

    async def delete_alert_type(self, alert_type_id: int) -> BasicResponse[None]:
        try:
            await self._service.delete_alert_type(alert_type_id)
            return BasicResponse[None](data=None)
        except HTTPException as http_ex:
            await self._session.rollback()
            raise http_ex
        except Exception as e:
            await self._session.rollback()
            print(f"Erro ao deletar tipo de alerta: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )
