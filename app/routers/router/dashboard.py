from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.dashboard import DashboardController
from app.schemas.dashboard import (
    AlertCounts,
    AlertTypeDistributionItem,
    MeasuresStatusItem,
    StationHistoryItem,
    StationStatus,
)

router = APIRouter(tags=["Dashboard"], prefix="/dashboard")


@router.get(
    "/station-history", response_model=BasicResponse[list[StationHistoryItem]]
)
async def get_station_history(
    station_id: int | None = Query(default=None, description="Optional station ID"),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[StationHistoryItem]]:
    return await DashboardController(session).get_station_history(station_id)


@router.get(
    "/alert-types", response_model=BasicResponse[list[AlertTypeDistributionItem]]
)
async def get_alert_type_distribution(
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[AlertTypeDistributionItem]]:
    return await DashboardController(session).get_alert_type_distribution()


@router.get("/alert-counts", response_model=BasicResponse[AlertCounts])
async def get_alert_counts(
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[AlertCounts]:
    return await DashboardController(session).get_alert_counts()


@router.get("/station-status", response_model=BasicResponse[StationStatus])
async def get_station_status(
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[StationStatus]:
    return await DashboardController(session).get_station_status()


@router.get(
    "/measures-status", response_model=BasicResponse[list[MeasuresStatusItem]]
)
async def get_measures_status(
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[MeasuresStatusItem]]:
    return await DashboardController(session).get_measures_status()
