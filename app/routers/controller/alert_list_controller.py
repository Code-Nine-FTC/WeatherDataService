# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.dependency import get_db_session
from app.schemas.alert_schema import AlertResponse
from app.service.alert_list_service import AlertListService

router = APIRouter()


@router.get("/alert/list", response_model=List[AlertResponse])
async def list_alerts(session: AsyncSession = Depends(get_db_session)):
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
    date_inicial: Optional[datetime] = Query(None),
    date_final: Optional[datetime] = Query(None),
    station_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_db_session),
):
    service = AlertListService(session)
    try:
        return await service.get_filtered_alerts(
            date_inicial, date_final, station_id
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar alertas filtrados.",
        )
