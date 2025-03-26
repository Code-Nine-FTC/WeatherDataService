# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependency.auth import AuthManager
from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.alert import AlertController
from app.schemas.alert import RequestAlert

router = APIRouter(tags=["Alertas"],prefix="/alert")

@router.delete("/id", 
dependencies=[Depends(AuthManager.has_authorization)])
async def delete_alert(
    alert_data: RequestAlert,
    session: AsyncSession = Depends(SessionConnection.session), 
) -> BasicResponse[None]:
    return await AlertController(session).delete_alert(alert_data)
