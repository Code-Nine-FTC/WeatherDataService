# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.exemple import ExempleController
from app.schemas.exemple import ResponseExempleService

router = APIRouter(tags=["example"], prefix="/example")


@router.get("/")
def hello_world() -> dict[str, str]:
    return {"msg": "Hello World"}


@router.get("/select")
async def exemple_select(
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[ResponseExempleService]:
    return await ExempleController(session).run()
