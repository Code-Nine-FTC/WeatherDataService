from typing import List, Optional

from fastapi import APIRouter, Depends, Query
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
