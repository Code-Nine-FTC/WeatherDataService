# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.alert_type_controller import AlertTypeController
from app.schemas.alert_type_schema import AlertTypeCreate

router = APIRouter(tags=["Tipos de alerta"], prefix="/alert_type")


@router.post("/create")
async def create_alert_type(
    alert_type_data: AlertTypeCreate,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[None]:
    return await AlertTypeController(session).create_alert_type(alert_type_data)
