# -*- coding: utf-8 -*-

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.basic_response import BasicResponse
from app.schemas.user_view_schema import UserViewResponse
from app.service.user import UserService


class UserController:
    def __init__(self, session: AsyncSession, user: UserViewResponse) -> None:
        self._service = UserService(session)
        self._user = user

    async def get_user(self) -> BasicResponse[UserViewResponse]:
        try:
            user = await self._service.get_user_by_email(self._user.email)
            return BasicResponse(data=user)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise e
