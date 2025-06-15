# -- coding: utf-8 --

from datetime import datetime, timezone
from typing import AsyncGenerator
from sqlalchemy import text

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_model import (
    Alert,
    Measures,
    Parameter,
    ParameterType,
    TypeAlert,
    WeatherStation,
)

@pytest_asyncio.fixture
async def delete_all_stations(
    db_session: AsyncSession
) -> AsyncGenerator[None, None]:
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