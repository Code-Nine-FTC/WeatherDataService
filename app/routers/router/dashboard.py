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
    "/station-history/{station_id}", response_model=BasicResponse[list[StationHistoryItem]]
)
async def get_station_history(
    station_id: int,
    startDate: str | None = Query(default=None, description="Data de início da filtragem"),
    endDate: str | None = Query(default=None, description="Data de fim da filtragem"),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[StationHistoryItem]]:
    return await DashboardController(session
        ).get_station_history(station_id, startDate, endDate)


@router.get("/alert-types", response_model=BasicResponse[list[AlertTypeDistributionItem]])
async def get_alert_type_distribution(
    station_id: int | None = Query(default=None, description="ID da estação"),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[AlertTypeDistributionItem]]:
    return await DashboardController(session).get_alert_type_distribution(station_id)


@router.get("/alert-counts", response_model=BasicResponse[AlertCounts])
async def get_alert_counts(
    station_id: int | None = Query(default=None, description="ID da estação"),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[AlertCounts]:
    return await DashboardController(session).get_alert_counts(station_id)


@router.get("/station-status", response_model=BasicResponse[StationStatus])
async def get_station_status(
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[StationStatus]:
    return await DashboardController(session).get_station_status()


@router.get("/measures-status", response_model=BasicResponse[list[MeasuresStatusItem]])
async def get_measures_status(
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[MeasuresStatusItem]]:
    return await DashboardController(session).get_measures_status()


@router.get("/last-measures/{station_id}", 
    response_model=BasicResponse[list[StationHistoryItem]])
async def get_last_measures(
    station_id: int,
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[list[StationHistoryItem]]:
    return await DashboardController(session).get_last_measures(station_id)
