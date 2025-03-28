from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.parameter_type import ParameterTypeCreate
from app.service.parameter_type import ParameterTypeService


class ParameterTypeController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._service = ParameterTypeService(session)

    async def create_parameter_type(
        self, parameter_type_data: ParameterTypeCreate
    ) -> BasicResponse[None]:
        try:
            await self._service.create_parameter_type(parameter_type_data)
            return BasicResponse[None](data=None)
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            print(f"Erro ao criar tipo de parâmetro: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor, tente novamente mais tarde.",
            )
