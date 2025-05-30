# -*- coding: utf-8 -*-
from fastapi import FastAPI

from app.routers.router.alert import router_alert
from app.routers.router.alert_type import router as router_alert_type
from app.routers.router.auth import router as router_auth
from app.routers.router.dashboard import router as router_dashboard
from app.routers.router.parameter_type import router as router_parameter_type
from app.routers.router.user import router as router_user
from app.routers.router.weather_station import router as router_weather_station


def define_routes(app: FastAPI) -> None:
    app.include_router(router_weather_station)
    app.include_router(router_alert_type)
    app.include_router(router_parameter_type)
    app.include_router(router_user)
    app.include_router(router_auth)
    app.include_router(router_alert)
    app.include_router(router_dashboard)
