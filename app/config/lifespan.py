# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from app.dependency.database import Database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    try:
        await Database().ping()
        yield
    finally:
        await Database().close()
