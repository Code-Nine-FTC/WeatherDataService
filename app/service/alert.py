# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.alert import RequestAlert
from app.core.models.db_model import Alert

class AlertService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def delete_alert(self, id_alert: RequestAlert) -> None:
        result = await self._session.execute(select(Alert).where(Alert.id == id_alert.id)) 
        alert = result.scalars().first()
        if alert is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta com a ID {id_alert.id} não encontrado.",
            )
        await self._session.delete(alert)
        await self._session.commit()

