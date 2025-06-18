# -- coding: utf-8 --

from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture
async def delete_all_stations(db_session: AsyncSession) -> AsyncGenerator[None, None]:
    try:
        await db_session.execute(text("DELETE FROM weather_stations"))
        await db_session.commit()
    except Exception:
        await db_session.rollback()
        raise
    yield
    try:
        await db_session.execute(text("DELETE FROM weather_stations"))
        await db_session.commit()
    except Exception:
        await db_session.rollback()
        raise
