import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, text, update
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
    ) -> list[ParameterTypeResponse]:
        query = text(
            f"""
            select
            pt.id,
            pt."name",
            pt.detect_type,
            pt.factor,
            pt."offset",
            pt.measure_unit,
            pt.qnt_decimals,
            pt.is_active
            from parameter_types pt
            where 1=1
            {"and pt.name like :name" if filters and filters.name else ""}
            {"and pt.is_active = :is_active" if filters and filters.is_active else ""}
    """
        )
        if filters and filters.name:
            query = query.bindparams(name=f"%{filters.name}%")
        if filters and filters.is_active is not None:
            query = query.bindparams(is_active=filters.is_active)

        result = await self._session.execute(query)
        parameter_types = result.fetchall()
        return [ParameterTypeResponse(**pt._asdict()) for pt in parameter_types]

    async def delete_parameter_type(self, parameter_type_id: int) -> None:
        parameter_type = await self._search_parameter_type_id(parameter_type_id)
        await self._session.execute(
            update(ParameterType)
            .where(ParameterType.id == parameter_type.id)
            .values(is_active=False, last_update=datetime.now())
        )
        await self._session.commit()

    async def get_parameter_type(self, parameter_type_id: int) -> ParameterTypeResponse:
        parameter_type = await self._session.get(ParameterType, parameter_type_id)
        if parameter_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de parâmetro com a ID {parameter_type_id} não encontrado.",
            )

        return ParameterTypeResponse.model_validate(parameter_type, from_attributes=True)

    async def update_parameter_type(
        self,
        parameter_type_id: int,
        data: UpdateParameterType,
    ) -> None:
        parameter_type = await self._session.get(ParameterType, parameter_type_id)
        if parameter_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de parâmetro com a ID {parameter_type_id} não encontrado.",
            )

        data_update = {k: v for k, v in data.model_dump().items() if v is not None}

        await self._session.execute(
            update(ParameterType)
            .where(ParameterType.id == parameter_type_id)
            .values(**data_update)
        )
        await self._session.commit()

    async def _search_parameter_type_id(self, parameter_type_id: int) -> ParameterType:
        query = text("SELECT * FROM parameter_types WHERE id = :parameter_type_id").bindparams(
            parameter_type_id=parameter_type_id
        )
        result = await self._session.execute(query)
        parameter_type = result.fetchone()
        if parameter_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de parâmetro com a ID {parameter_type_id} não encontrado.",
            )
        return ParameterType(**parameter_type._asdict())

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
        return result.scalar_one_or_none()
