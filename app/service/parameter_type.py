from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, update, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_model import ParameterType
from app.schemas.parameter_type import (
    CreateParameterType,
    FilterParameterType,
    ParameterTypeResponse,
    UpdateParameterType,
)


class ParameterTypeService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_parameter_type(self, data: CreateParameterType) -> None:
        parameter = await self._search_parameter_type(
            data.name,
            data.measure_unit,
            data.qnt_decimals,
            data.offset,
            data.factor,
        )
        if parameter:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de parâmetro já existe.",
            )
        parameter_type = ParameterType(**data.model_dump())
        self._session.add(parameter_type)
        await self._session.flush()
        await self._session.commit()

    async def list_parameter_types(
        self, filters: FilterParameterType | None = None
    ) -> List[ParameterTypeResponse]:
        query = text(
            f"""
            select 
            pt.id,
            pt."name",
            pt.factor,
            pt."offset" ,
            pt.measure_unit,
            pt.qnt_decimals 
            from parameter_types pt
            where 1=1
            {"and pt.name like :name" if filters and filters.name else ""}
            {"and pt.measure_unit like :measure_unit" if filters and filters.measure_unit else ""}
    """
        )
        if filters and filters.name:
            query = query.bindparams(name=f"%{filters.name}%")
        if filters and filters.measure_unit:
            query = query.bindparams(measure_unit=f"%{filters.measure_unit}%")
        result = await self._session.execute(query)
        parameter_types = result.fetchall()
        return [ParameterTypeResponse(**pt._asdict()) for pt in parameter_types]

    async def get_parameter_type(
        self, parameter_type_id: int
    ) -> ParameterTypeResponse:
        parameter_type = self._search_parameter_type_id(parameter_type_id)
        return ParameterTypeResponse(**parameter_type.__dict__)

    async def update_parameter_type(
        self,
        parameter_type_id: int,
        data: UpdateParameterType,
    ) -> None:
        parameter_type = await self._search_parameter_type_id(parameter_type_id)
        data = {k: v for k, v in data.model_dump().items() if v is not None}
        self._session.execute(
            update(ParameterType)
            .where(ParameterType.id == parameter_type.id)
            .values(**data)
        )
        await self._session.commit()

    async def _search_parameter_type_id(
        self, parameter_type_id: int
    ) -> ParameterType:
        parameter_type = await self._session.get(ParameterType, parameter_type_id)
        if parameter_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de parâmetro com a ID {parameter_type_id} não encontrado.",
            )
        return parameter_type

    async def _search_parameter_type(
        self,
        name: str,
        measure_unit: str,
        qnt_decimals: int,
        offset: float | None,
        factor: float | None,
    ) -> ParameterType | None:
        query = select(ParameterType).where(
            ParameterType.name == name,
            ParameterType.measure_unit == measure_unit,
            ParameterType.qnt_decimals == qnt_decimals,
            ParameterType.offset == offset,
            ParameterType.factor == factor,
        )
        result = await self._session.execute(query)
        parameter_type = result.scalar_one_or_none()
        return parameter_type
