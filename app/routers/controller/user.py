# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.user import UserResponse
from app.service.user import UserService


class UserController:
    def __init__(self, session: AsyncSession, user: UserResponse) -> None:
        self._service = UserService(session)
        self._user = user

    async def get_user(self) -> BasicResponse[UserResponse]:
        try:
            user = await self._service.get_user_by_email(self._user.email)
            return BasicResponse(data=user)
        except Exception as e:
            raise e
