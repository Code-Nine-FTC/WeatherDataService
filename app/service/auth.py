# -*- coding: utf-8 -*-
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.security import PasswordManager, TokenManager
from app.schemas.auth import Token
from app.schemas.user import UserResponse
from app.service.user import UserService


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.__pwd_manager = PasswordManager()
        self.__token_manager = TokenManager()
        self._service_user = UserService(session)

    async def login(self, form_data: OAuth2PasswordRequestForm) -> Token:
        user: UserResponse | None = await self._service_user.get_user_by_email(
            form_data.username
        )
        if not user or not self.__pwd_manager.verify_password(
            form_data.password, user.password
        ):
            raise HTTPException(
                status_code=400, detail="Nome de usuário ou senha incorretos"
            )
        access_token = self.__token_manager.create_access_token(user)
        return Token(access_token=access_token, token_type="bearer")
