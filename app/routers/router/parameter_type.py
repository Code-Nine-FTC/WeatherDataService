
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.parameter_type import ParameterTypeController
from app.schemas.parameter_type import CreateParameterType, ParameterTypeResponse, FilterParameterType

router = APIRouter(tags=["Parameter Types"], prefix="/parameter_types")


@router.post("/")
async def create_parameter_type(
    data: CreateParameterType,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[None]:
    return await ParameterTypeController(session).create_parameter_type(data)


@router.get("/")
async def list_parameter_types(
    filters: FilterParameterType = Query(),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[ParameterTypeResponse]]:
    return await ParameterTypeController(session).list_parameter_types(
        filters
    )


# @router.get("/{parameter_type_id}")
# async def get_parameter_type(
#     parameter_type_id: int,
#     session: AsyncSession = Depends(SessionConnection.session),
# ) -> ParameterTypeResponse:
#     parameter_type = await ParameterTypeController(session).get_parameter_type(
#         parameter_type_id
#     )
#     if not parameter_type:
#         raise HTTPException(
#             status_code=404, detail="Tipo de parâmetro não encontrado."
#         )
#     return parameter_type


# class ParameterTypeUpdate(BaseModel):
#     name: Optional[str] = None
#     measure_unit: Optional[str] = None
#     qnt_decimals: Optional[int] = None
#     offset: Optional[float] = None
#     factor: Optional[float] = None


# @router.patch("/{parameter_type_id}")
# async def update_parameter_type(
#     parameter_type_id: int,
#     data: ParameterTypeUpdate,
#     session: AsyncSession = Depends(SessionConnection.session),
# ) -> None:
#     await ParameterTypeController(session).update_parameter_type(
#         parameter_type_id, data.dict(exclude_unset=True)
#     )
