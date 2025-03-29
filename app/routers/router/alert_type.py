# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.auth import AuthManager
from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.alert_type import AlertTypeController
from app.schemas.alert_type_schema import (
    AlertTypeCreate,
    AlertTypeResponse,
    AlertTypeUpdate,
)

router = APIRouter(tags=["Tipos de alerta"], prefix="/alert_type", dependencies=[Depends(AuthManager.has_authorization)])



@router.post("/")
async def create_alert_type(
    alert_type_data: AlertTypeCreate,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[None]:
    return await AlertTypeController(session).create_alert_type(alert_type_data)


@router.get("/")
async def list_alert_types(
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[AlertTypeResponse]]:
    return await AlertTypeController(session).list_alert_types()


@router.get("/{alert_type_id}")
async def get_alert_type(
    alert_type_id: int, session: AsyncSession = Depends(SessionConnection.session)
) -> BasicResponse[AlertTypeResponse]:
    return await AlertTypeController(session).get_alert_type(alert_type_id)


dependencies = ([Depends(AuthManager.has_authorization)],)


@router.patch("/{alert_type_id}")
async def update_alert_type(
    alert_type_id: int,
    alert_type_data: AlertTypeUpdate,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[None]:
    return await AlertTypeController(session).update_alert_type(
        alert_type_id, alert_type_data
    )


dependencies = ([Depends(AuthManager.has_authorization)],)


@router.patch("/disables/{alert_type_id}")
async def delete_alert_type(
    alert_type_id: int, session: AsyncSession = Depends(SessionConnection.session)
) -> BasicResponse[None]:
    return await AlertTypeController(session).delete_alert_type(alert_type_id)
