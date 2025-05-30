# -*- coding: utf-8 -*-

from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.pool import NullPool

from app.config.settings import Settings
from app.modules.common import Singleton


class Database(metaclass=Singleton):
    def __init__(self) -> None:
        self._engine: AsyncEngine = self._create_engine()  # type: ignore[assignment]
        self._session_maker: async_sessionmaker[AsyncSession] = self._create_session_factory()

    async def ping(self) -> None:
        async with self.session as session:
            await session.execute(text("SELECT 1;"))

    @property
    def session(self) -> AsyncSession:
        return self._session_maker()  # type: ignore[no-any-return,operator, unused-ignore] # noqa

    def _create_engine(self) -> async_sessionmaker[AsyncSession]:  # noqa: PLR6301
        return create_async_engine(
            Settings().DATABASE_URL,  # type: ignore[return-value, call-arg]
            poolclass=NullPool if Settings().TEST_ENV else None,  # type: ignore[return-value, call-arg]
            pool_size=150,  # 150 para 200 conexões simultâneas
            max_overflow=50,  # 50 para 200 conexões simultâneas
            pool_timeout=30,
            pool_recycle=1800,
        )

    def _create_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def close(self) -> None:
        await self._engine.dispose()


class SessionConnection:
    @staticmethod
    async def session() -> AsyncGenerator[AsyncSession, None]:
        async with Database().session as session:
            yield session
