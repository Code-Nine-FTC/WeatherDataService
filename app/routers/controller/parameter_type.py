from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.parameter_type import (
    CreateParameterType,
    ParameterTypeResponse,
)
from app.service.parameter_type import ParameterTypeService


class ParameterTypeController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = ParameterTypeService(session)
        self._session = session

    async def create_parameter_type(
        self, data: CreateParameterType
    ) -> BasicResponse[None]:
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
        self, name: Optional[str] = None, measure_unit: Optional[str] = None
    ) -> List[ParameterTypeResponse]:
        return await self._service.list_parameter_types(name, measure_unit)

    async def update_parameter_type(
        self,
        parameter_type_id: int,
        data: Dict[str, Any],  # Especifica os tipos do dicionário
    ) -> None:
        await self._service.update_parameter_type(parameter_type_id, data)

    async def get_parameter_type(
        self, parameter_type_id: int
    ) -> Optional[ParameterTypeResponse]:
        return await self._service.get_parameter_type(parameter_type_id)
