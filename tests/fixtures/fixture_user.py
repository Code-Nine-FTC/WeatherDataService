# -*- coding: utf-8 -*-

from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models.db_model import User
from app.modules.security import PasswordManager
from tests.fixtures.fixture_insert import db_session


@pytest_asyncio.fixture
async def fake_user(db_session: AsyncSession) -> AsyncGenerator[User, None]:
    query = select(User).where(User.email == "test_user@example.com")
    result = await db_session.execute(query)
    user = result.scalars().first()

    if not user:
        hashed_password = PasswordManager().password_hash("123")
        user = User(name="test_user", email="test_user@example.com", password=hashed_password)
        db_session.add(user)
        await db_session.commit()

    yield user
    await db_session.delete(user)
    await db_session.commit()
