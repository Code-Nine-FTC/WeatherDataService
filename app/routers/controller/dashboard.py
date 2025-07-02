from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.dashboard import (
    AlertCounts,
    AlertTypeDistributionItem,
    MeasuresStatusItem,
    StationHistoryItem,
    StationStatus,
)
from app.service.dashboard import DashboardService


class DashboardController:
    def __init__(self, session: AsyncSession):
        self._service = DashboardService(session)

    async def get_station_history(
        self, station_id: int, start_date: str | None = None, end_date: str | None = None
    ) -> BasicResponse[list[StationHistoryItem]]:
        try:
            data = await self._service.get_station_history(station_id, start_date, end_date)
            return BasicResponse(data=[StationHistoryItem(**row._asdict()) for row in data])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar histórico da estação: {str(e)}",
            )

    async def get_alert_type_distribution(
        self,
        station_id: int | None = None,
    ) -> BasicResponse[list[AlertTypeDistributionItem]]:
        try:
            data = await self._service.get_alert_type_distribution(station_id)
            return BasicResponse(
                data=[AlertTypeDistributionItem(**row._asdict()) for row in data]
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar distribuição de alertas: {str(e)}",
            )

    async def get_alert_counts(
        self, station_id: int | None = None
    ) -> BasicResponse[AlertCounts]:
        try:
            data = await self._service.get_alert_counts(station_id)
            return BasicResponse(data=AlertCounts(**data))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar contagem de alertas: {str(e)}",
            )

    async def get_station_status(self) -> BasicResponse[StationStatus]:
        try:
            data = await self._service.get_station_status()
            return BasicResponse(data=StationStatus(**data))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar status das estações: {str(e)}",
            )

    async def get_measures_status(self) -> BasicResponse[list[MeasuresStatusItem]]:
        try:
            data = await self._service.get_measures_status()
            return BasicResponse(
                data=[MeasuresStatusItem(label=row.label, number=row.number) for row in data]
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar status das medidas: {str(e)}",
            )

    async def get_last_measures(
        self, station_id: int
    ) -> BasicResponse[list[StationHistoryItem]]:
        try:
            data = await self._service.get_last_measures(station_id)
            return BasicResponse(data=[StationHistoryItem(**row._asdict()) for row in data])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar últimas medidas dashboard: {str(e)}",
            )
