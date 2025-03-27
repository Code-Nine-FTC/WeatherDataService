# -*- coding: utf-8 -*-
from fastapi import FastAPI

from app.routers.router.alert_type import router as router_alert_type
from app.routers.router.parameter_type import router as router_parameter_type
from app.routers.router.weather_station import router


def define_routes(app: FastAPI) -> None:
    app.include_router(router)
    app.include_router(router_alert_type)
    app.include_router(router_parameter_type)
