from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.parameter_type import (
    CreateParameterType,
    ParameterTypeResponse,
)
from app.service.parameter_type import FilterParameterType, ParameterTypeService


class ParameterTypeController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = ParameterTypeService(session)
        self._session = session

    async def create_parameter_type(self, data: CreateParameterType) -> BasicResponse[None]:
        try:
            await self._service.create_parameter_type(data)
            return BasicResponse[None](data=None)
        except HTTPException as e:
            await self._session.rollback()
            raise HTTPException(
                status_code=e.status_code,
                detail=f"Erro ao criar o tipo de parâmetro: {e.detail}",
            )
        except Exception as e:
            await self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao criar o tipo de parâmetro: {str(e)}",
            )

    async def list_parameter_types(
        self, filters: FilterParameterType
    ) -> BasicResponse[list[ParameterTypeResponse]]:
        try:
            parameter_types = await self._service.list_parameter_types(filters)
            return BasicResponse(data=parameter_types)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao listar os tipos de parâmetro: {str(e)}",
            )

    async def update_parameter_type(
        self,
        parameter_type_id: int,
        data: dict[str, Any],
    ) -> BasicResponse[None]:
        try:
            await self._service.update_parameter_type(parameter_type_id, data)
            return BasicResponse[None](data=None)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise e

    async def get_parameter_type(
        self, parameter_type_id: int
    ) -> BasicResponse[ParameterTypeResponse]:
        try:
            parameter_type = await self._service.get_parameter_type(parameter_type_id)
            return BasicResponse[ParameterTypeResponse](data=parameter_type)
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            raise e

    async def disable_parameter_type(self, parameter_type_id: int) -> BasicResponse[None]:
        try:
            await self._service.delete_parameter_type(parameter_type_id)
            return BasicResponse[None](data=None)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao desativar o tipo de parâmetro: {str(e)}",
            )
