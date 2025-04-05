# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.auth import AuthManager
from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.alert import AlertController
from app.schemas.alert import (
    AlertFilterSchema,
    AlertResponse,
)

router_alert = APIRouter(tags=["Alertas"], prefix="/alert")


@router_alert.get("/all")
async def get_filtered_alerts(
    filters: AlertFilterSchema = Query(),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[AlertResponse]]:
    return await AlertController(session).get_filtered_alerts(filters)


@router_alert.delete("/{alert_id}", dependencies=[Depends(AuthManager.has_authorization)])
async def delete_alert(
    alert_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[None]:
    return await AlertController(session).delete_alert(alert_id)


@router_alert.get("/{alert_id}")
async def get_alert_by_id(
    alert_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[AlertResponse]:
    return await AlertController(session).get_alert_by_id(alert_id)
