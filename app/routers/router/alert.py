# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.auth import AuthManager
from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.alert import AlertController
from app.schemas.alert import RequestAlert

router_alert = APIRouter(tags=["Alertas"], prefix="/alert")


@router_alert.delete("/", dependencies=[Depends(AuthManager.has_authorization)])
async def delete_alert(
    alert_data: RequestAlert,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[None]:
    return await AlertController(session).delete_alert(alert_data)


@router_alert.get("/", dependencies=[Depends(AuthManager.has_authorization)])
async def get_alert_by_id(
    alert_data: RequestAlert,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[RequestAlert]:
    return await AlertController(session).get_alert_by_id(alert_data)


@router_alert.get("/all")
async def get_alerts(
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[RequestAlert]]:
    return await AlertController(session).get_alerts()


@router_alert.get("/filter")
async def get_filtered_alerts(
    filters: RequestAlert = Query(),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[RequestAlert]]:
    return await AlertController(session).get_filtered_alerts(filters)


@router_alert.post("/")
async def create_alert(
    alert_data: RequestAlert,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[RequestAlert]:
    return await AlertController(session).create_alert(alert_data)
