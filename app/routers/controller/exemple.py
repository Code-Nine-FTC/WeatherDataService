# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.exemple import ResponseExempleService
from app.service.exemple import ServiceExemple


class ExempleController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._result: ResponseExempleService | None = None
        self._service = ServiceExemple(session)

    async def run(self) -> BasicResponse[ResponseExempleService]:
        try:
            self._result = await self._service.run()
            if self._result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return BasicResponse[ResponseExempleService](data=self._result)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
