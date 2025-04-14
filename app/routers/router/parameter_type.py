from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.parameter_type import ParameterTypeController
from app.schemas.parameter_type import (
    CreateParameterType,
    FilterParameterType,
    ParameterTypeResponse,
    UpdateParameterType,
)

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
    return await ParameterTypeController(session).list_parameter_types(filters)


@router.patch("/{parameter_type_id}")
async def delete_parameter_type(
    parameter_type_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[None]:
    return await ParameterTypeController(session).disable_parameter_type(parameter_type_id)


@router.get("/{parameter_type_id}")
async def get_parameter_type(
    parameter_type_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[ParameterTypeResponse]:
    return await ParameterTypeController(session).get_parameter_type(
        parameter_type_id)


@router.patch("/{parameter_type_id}/update")
async def update_parameter_type(
    parameter_type_id: int,
    data: UpdateParameterType,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[None]:
    await ParameterTypeController(session).update_parameter_type(parameter_type_id, data)
    return BasicResponse(data=None)
