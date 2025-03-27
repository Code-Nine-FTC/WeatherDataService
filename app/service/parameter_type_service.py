from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
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
                offset=int(pt.offset)
                if pt.offset is not None
                else None,  # Conversão para int
                factor=int(pt.factor)
                if pt.factor is not None
                else None,  # Conversão para int
                name=pt.name,
            )
            for pt in parameter_types
        ]

    async def get_parameter_type(
        self, parameter_type_id: int
    ) -> Optional[ParameterTypeResponse]:
        query = select(ParameterType).where(ParameterType.id == parameter_type_id)
        result = await self._session.execute(query)
        parameter_type = result.scalar_one_or_none()

        if not parameter_type:
            return None

        return ParameterTypeResponse(
            name=parameter_type.name,
            measure_unit=parameter_type.measure_unit,
            qnt_decimals=parameter_type.qnt_decimals,
            offset=int(parameter_type.offset) if parameter_type.offset is not None else None,
            factor=int(parameter_type.factor) if parameter_type.factor is not None else None,
        )

    async def update_parameter_type(
        self, parameter_type_id: int, data: Dict[str, Any]  # Especifica os tipos do dicionário
    ) -> None:
        # Buscar o tipo de parâmetro pelo ID
        query = select(ParameterType).where(ParameterType.id == parameter_type_id)
        result = await self._session.execute(query)
        parameter_type = result.scalar_one_or_none()

        if not parameter_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de parâmetro não encontrado.",
            )

        # Verificar se as novas informações são iguais às atuais
        if all(getattr(parameter_type, key) == value for key, value in data.items()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="As informações fornecidas são iguais às atuais.",
            )

        # Verificar se já existe um tipo de parâmetro com as mesmas informações
        query = select(ParameterType).where(
            ParameterType.name == data.get("name"),
            ParameterType.measure_unit == data.get("measure_unit"),
            ParameterType.qnt_decimals == data.get("qnt_decimals"),
            ParameterType.offset == data.get("offset"),
            ParameterType.factor == data.get("factor"),
            ParameterType.id != parameter_type_id,
        )
        result = await self._session.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um tipo de parâmetro com as mesmas informações.",
            )

        # Atualizar os campos
        for key, value in data.items():
            setattr(parameter_type, key, value)
        parameter_type.last_update = datetime.now()

        # Salvar as alterações
        await self._session.commit()
