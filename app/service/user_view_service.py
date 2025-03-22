from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.db_model import User
from app.schemas.user_view_schema import UserViewResponse


class UserViewService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_id(self, user_id: int) -> UserViewResponse:
        user = await self._session.get(User, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado.",
            )

        return UserViewResponse(
            name=user.name, email=user.email, last_update=user.last_update
        )
