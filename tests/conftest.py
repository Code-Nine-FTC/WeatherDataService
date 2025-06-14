# -- coding: utf-8 --


from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.settings import settings
from app.core.models.db_model import (
    User,
)
from app.dependency.database import Database
from app.modules.security import PasswordManager, TokenManager
from app.schemas.user import UserResponse
from main import app
from tests.fixtures.fixture_insert import (
    alerts_fixture,  # noqa: F401
    measures_fixture,  # noqa: F401
    parameter_types_fixture,  # noqa: F401
    parameters_fixture,  # noqa: F401
    type_alerts_fixture,  # noqa: F401
    weather_stations_fixture,  # noqa: F401
)


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


@pytest_asyncio.fixture
async def authenticated_client(fake_user: User) -> AsyncGenerator[AsyncClient, None]:
    user_response = UserResponse.model_validate(fake_user)
    token = TokenManager().create_access_token(user_response)
    headers = {"Authorization": f"Bearer {token}"}
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://localhost:5000", headers=headers
    ) as ac:
        yield ac


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    settings.DATABASE_URL = settings.DATABASE_URL_TEST
    async with Database().session as session:
        yield session
    await Database().close()
