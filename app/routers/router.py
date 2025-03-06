from fastapi import FastAPI
from app.routers.exemple import router

def define_routes(app: FastAPI):
    app.include_router(router)