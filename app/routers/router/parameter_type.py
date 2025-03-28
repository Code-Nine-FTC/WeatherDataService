from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.parameter_type import ParameterTypeController
from app.schemas.parameter_type import ParameterTypeCreate

router = APIRouter(tags=["Tipos de Parâmetro"], prefix="/parameter_type")


@router.post("/")
async def create_parameter_type(
    parameter_type_data: ParameterTypeCreate,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[None]:  # Alterado para retornar BasicResponse[None]
    return await ParameterTypeController(session).create_parameter_type(
        parameter_type_data
    )
