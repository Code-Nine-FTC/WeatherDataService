# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import bindparam, text

from app.schemas.user import UserResponse


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_email(self, email: str) -> UserResponse | None:
        query = text("""SELECT * FROM users WHERE email = :email""").bindparams(
            bindparam("email", email)
        )
        result = await self._session.execute(query)
        user = result.fetchone()
        return UserResponse(**user._asdict()) if user else None

    async def get_user_by_id(self, user_id: int) -> UserResponse | None:
        query = text("SELECT * FROM users WHERE id = :id").bindparams(
            bindparam("id", user_id)
        )
        result = await self._session.execute(query)
        user = result.fetchone()
        return UserResponse(**user._asdict()) if user else None
