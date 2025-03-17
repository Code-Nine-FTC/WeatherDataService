# -*- coding: utf-8 -*-
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import registry

from app.config.settings import Settings
from app.modules.common import Singleton

mapper_registry = registry()


class Database(metaclass=Singleton):
    def __init__(self) -> None:
        self._engine = create_async_engine(
            Settings().DATABASE_URL, echo=False, future=True
        )
        self.session_factory = async_sessionmaker(
            bind=self._engine, expire_on_commit=False, class_=AsyncSession
        )

    async def ping(self) -> None:
        async with self.session_factory() as session:
            await session.execute(text("SELECT 1;"))

    @staticmethod
    async def _create_engine() -> AsyncEngine:
        return create_async_engine(Settings().DATABASE_URL, echo=False, future=True)

    async def close(self) -> None:
        await self._engine.dispose()


class SessionConnection:
    @staticmethod
    async def session() -> AsyncGenerator[AsyncSession, None]:
        db = Database()
        async with db.session_factory() as session:
            yield session
