# -*- coding: utf-8 -*-


from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from testcontainers.postgres import PostgresContainer

from app.config.settings import settings
from app.core.models.db_model import Base
from app.modules.security import TokenManager
from main import app
from tests.fixtures.fixture_user import fake_user  # noqa: F401


@pytest.fixture(scope="function")  # noqa: PT003
def authenticated_client(fake_user) -> TestClient:  # noqa: F811  # type: ignore[no-untyped-def]
    client = TestClient(app, base_url="http://localhost:5000")
    token = TokenManager().create_access_token(fake_user)
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    with PostgresContainer("postgres:16") as postgres:
        db_url = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        settings.DATABASE_URL = db_url
        # Cria a engine assíncrona
        engine = create_async_engine(db_url, poolclass=NullPool, echo=True)

        # Cria as tabelas usando o metadata do Base
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Cria a sessão assíncrona
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

        async with async_session() as session:
            yield session  # Sessão pronta para uso nos testes
            await session.rollback()  # Rollback para limpar

        # Limpa as tabelas após os testes (opcional)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
