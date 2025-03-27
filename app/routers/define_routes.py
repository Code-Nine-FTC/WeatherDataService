# -*- coding: utf-8 -*-
from fastapi import FastAPI

from app.routers.router.alert import router as router_alert
from app.routers.router.alert_type import router as router_alert_type
from app.routers.router.auth import router as router_auth
from app.routers.router.user_view import router as router_user_view
from app.routers.router.weather_station import router as router_weather_station


def define_routes(app: FastAPI) -> None:
    app.include_router(router_weather_station)
    app.include_router(router_alert_type)
    app.include_router(router_user_view)
    app.include_router(router_auth)
    app.include_router(router_alert)
