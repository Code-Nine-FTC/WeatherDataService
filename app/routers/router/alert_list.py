# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.alert_list_controller import AlertListController
from app.schemas.alert_schema import AlertResponse

router = APIRouter(tags=["Alertas"], prefix="/alert")


@router.get("/list")
async def list_alerts(
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[AlertResponse]]:
    return await AlertListController(session).list_alerts()


@router.get("/filter")
async def filter_alerts(
    date_inicial: str | None = None,
    date_final: str | None = None,
    station_id: int | None = None,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[AlertResponse]]:
    return await AlertListController(session).filter_alerts(
        date_inicial, date_final, station_id
    )
