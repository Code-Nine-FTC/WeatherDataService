# -*- coding: utf-8 -*-
from fastapi import FastAPI

from app.routers.weather_station import router


def define_routes(app: FastAPI) -> None:
    app.include_router(router)
