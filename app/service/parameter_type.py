from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models.db_model import Measures, ParameterType  # Corrigido conforme o erro
from app.schemas.parameter_type import ParameterTypeCreate


class ParameterTypeService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_parameter_type(self, data: ParameterTypeCreate) -> None:
        # Valida os dados recebidos
        data.validate_offset_factor()

        # Verificar se o nome do parâmetro já existe
        existing_parameter = await self._session.execute(
            select(ParameterType).filter_by(
                name=data.name
            )  # Usando Measures no lugar de ParameterType
        )

        if existing_parameter.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tipo de parâmetro com esse nome já existe.",
            )

        # Criação do tipo de parâmetro
        new_parameter_type = ParameterType(
            **data.dict()
        )  # Usando Measures ao invés de ParameterType

        # Adicionar e confirmar a transação
        self._session.add(new_parameter_type)
        await self._session.commit()
