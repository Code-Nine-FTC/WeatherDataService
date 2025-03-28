from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.routers.controller.parameter_type_controller import ParameterTypeController
from app.schemas.parameter_type_schema import ParameterTypeResponse

router = APIRouter(tags=["Parameter Types"], prefix="/parameter_types")


@router.get("/", response_model=List[ParameterTypeResponse])
async def list_parameter_types(
    name: Optional[str] = Query(None),
    measure_unit: Optional[str] = Query(None),
    session: AsyncSession = Depends(SessionConnection.session),
) -> List[ParameterTypeResponse]:
    return await ParameterTypeController(session).list_parameter_types(
        name, measure_unit
    )


@router.get("/{parameter_type_id}", response_model=ParameterTypeResponse)
async def get_parameter_type(
    parameter_type_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
) -> ParameterTypeResponse:
    parameter_type = await ParameterTypeController(session).get_parameter_type(
        parameter_type_id
    )
    if not parameter_type:
        raise HTTPException(
            status_code=404, detail="Tipo de parâmetro não encontrado."
        )
    return parameter_type


class ParameterTypeUpdate(BaseModel):
    name: Optional[str] = None
    measure_unit: Optional[str] = None
    qnt_decimals: Optional[int] = None
    offset: Optional[float] = None
    factor: Optional[float] = None


@router.patch("/{parameter_type_id}")
async def update_parameter_type(
    parameter_type_id: int,
    data: ParameterTypeUpdate,
    session: AsyncSession = Depends(SessionConnection.session),
) -> None:
    await ParameterTypeController(session).update_parameter_type(
        parameter_type_id, data.dict(exclude_unset=True)
    )
