from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.parameter_type import ParameterTypeResponse
from app.service.parameter_type import ParameterTypeService


class ParameterTypeController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = ParameterTypeService(session)

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
