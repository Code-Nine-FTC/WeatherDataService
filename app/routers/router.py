# -*- coding: utf-8 -*-
from fastapi import FastAPI

from app.routers.exemple import router


def define_routes(app: FastAPI) -> None:
    app.include_router(router)
