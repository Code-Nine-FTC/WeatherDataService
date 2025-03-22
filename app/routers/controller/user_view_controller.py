# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_view_schema import UserViewResponse
from app.service.user_view_service import UserViewService


class UserViewController:
    def __init__(self, session: AsyncSession) -> None:
        self._service = UserViewService(session)

    async def get_user(self, user_id: int) -> UserViewResponse:
        return await self._service.get_user_by_id(user_id)
