# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.schemas.exemple import ResponseExempleService


class ServiceExemple:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._result: ResponseExempleService | None = None

    async def run(
        self,
    ) -> ResponseExempleService | None:
        await self._exemple()
        return (
            self._result
            if isinstance(self._result, ResponseExempleService)
            else None
        )

    async def _exemple(self) -> None:
        query_result = await self._session.execute(text("SELECT 1 "))
        row_result = query_result.fetchone()
        result_dict = {"value": str(row_result)}
        self._result = ResponseExempleService(**result_dict) if row_result else None
