# -*- coding: utf-8 -*-
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import bindparam, text

from app.core.models.db_model import User
from app.schemas.user import UserResponse


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_email(self, email: str) -> UserResponse | None:
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        return UserResponse(**user.__dict__)

    async def get_user_by_id(self, user_id: int) -> UserResponse | None:
        query = text("SELECT * FROM users WHERE id = :id").bindparams(bindparam("id", user_id))
        result = await self._session.execute(query)
        user = result.fetchone()
        return UserResponse(**user._asdict()) if user else None
