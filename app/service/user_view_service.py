# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_view_schema import UserViewResponse


class UserViewService:
    def __init__(self, session: AsyncSession, user: UserViewResponse) -> None:
        self._session = session
        self._user = user

    async def get_user_by_id(self, user_id: int) -> UserViewResponse:
        return self._user