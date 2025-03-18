# -*- coding: utf-8 -*-
from fastapi import FastAPI

from app.routers.router.alert import router as router_alert
from app.routers.router.alert_type import router as router_alert_type
from app.routers.router.exemple import router


def define_routes(app: FastAPI) -> None:
    app.include_router(router)
    app.include_router(router_alert_type)
    app.include_router(router_alert)
