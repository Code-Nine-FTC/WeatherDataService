# -*- coding: utf-8 -*-

from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models.db_model import User
from app.modules.security import PasswordManager


@pytest_asyncio.fixture
async def fake_user(session: AsyncSession) -> AsyncGenerator[User, None]:
    query = select(User).where(User.email == "test_user@example.com")
    result = await session.execute(query)
    user = result.scalars().first()

    if not user:
        hashed_password = PasswordManager().password_hash("123")
        user = User(name="test_user", email="test_user@example.com", password=hashed_password)
        session.add(user)
        await session.commit()

    yield user
    await session.delete(user)
    await session.commit()
