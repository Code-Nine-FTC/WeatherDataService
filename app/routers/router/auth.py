# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.routers.controller.auth import AuthController
from app.schemas.auth import Token

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(SessionConnection.session),
) -> Token:
    return await AuthController(session).login(form_data)
