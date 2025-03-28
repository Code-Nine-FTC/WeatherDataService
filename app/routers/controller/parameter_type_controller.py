from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.parameter_type_schema import ParameterTypeResponse
from app.service.parameter_type_service import ParameterTypeService


class ParameterTypeController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = ParameterTypeService(session)

    async def list_parameter_types(
        self, name: Optional[str] = None, measure_unit: Optional[str] = None
    ) -> List[ParameterTypeResponse]:
        return await self._service.list_parameter_types(name, measure_unit)
