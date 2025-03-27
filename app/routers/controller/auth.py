# -*- coding: utf-8 -*-
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import Token
from app.service.auth import AuthService


class AuthController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._service_auth = AuthService(session)

    async def login(
        self,
        form_data: OAuth2PasswordRequestForm,
    ) -> Token:
        try:
            return await self._service_auth.login(form_data)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise e
