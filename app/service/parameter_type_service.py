from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_model import ParameterType
from app.schemas.parameter_type_schema import ParameterTypeResponse


class ParameterTypeService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_parameter_types(
        self, name: Optional[str] = None, measure_unit: Optional[str] = None
    ) -> List[ParameterTypeResponse]:
        query = select(ParameterType)

        # Adicionar filtros opcionais
        if name:
            query = query.where(ParameterType.name == name)
        if measure_unit:
            query = query.where(ParameterType.measure_unit == measure_unit)

        result = await self._session.execute(query)
        parameter_types = result.scalars().all()

        # Converter para o schema de resposta
        return [
            ParameterTypeResponse(
                measure_unit=pt.measure_unit,
                qnt_decimals=pt.qnt_decimals,
                offset=int(pt.offset) if pt.offset is not None else None,  # Conversão para int
                factor=int(pt.factor) if pt.factor is not None else None,  # Conversão para int
                name=pt.name,
            )
            for pt in parameter_types
        ]