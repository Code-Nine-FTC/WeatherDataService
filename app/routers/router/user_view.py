from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.database import SessionConnection
from app.modules.auth.auth_manager import AuthManager
from app.modules.basic_response import BasicResponse
from app.routers.controller.user_view_controller import UserViewController
from app.schemas.user_view_schema import UserViewResponse

router = APIRouter(tags=["Usuários"], prefix="/user")


@router.get("/{id}")
async def get_user_by_id(
    id: int,
    user: UserViewResponse = Depends(AuthManager.has_authorization),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[UserViewResponse]:
    return await UserViewController(session, user).get_user(id)
