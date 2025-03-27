# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.auth_manager import AuthManager
from app.modules.dependency import get_db_session
from app.schemas.alert_list_schema import AlertFilterSchema, AlertResponse
from app.schemas.user_view_schema import UserViewResponse
from app.service.alert_list_service import AlertListService

router = APIRouter()


@router.get("/alert/list", response_model=List[AlertResponse])
async def list_alerts(
    session: AsyncSession = Depends(get_db_session),
    user: UserViewResponse = Depends(AuthManager.has_authorization),
):
    service = AlertListService(session)
    try:
        return await service.get_alerts()
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar alertas.",
        )


@router.get("/alert/filter", response_model=List[AlertResponse])
async def filter_alerts(
    filters: AlertFilterSchema = Depends(),
    session: AsyncSession = Depends(get_db_session),
    user: UserViewResponse = Depends(AuthManager.has_authorization),
):
    service = AlertListService(session)
    try:
        return await service.get_filtered_alerts(filters)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar alertas filtrados.",
        )
