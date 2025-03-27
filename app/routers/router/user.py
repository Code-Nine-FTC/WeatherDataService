from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.auth import AuthManager
from app.dependency.database import SessionConnection
from app.modules.basic_response import BasicResponse
from app.routers.controller.user import UserController
from app.schemas.user_view_schema import UserViewResponse

router = APIRouter(tags=["Usuários"], prefix="/user")


@router.get("/")
async def get_user(
    user: UserViewResponse = Depends(AuthManager.has_authorization),
    session: AsyncSession = Depends(SessionConnection.session),
) -> BasicResponse[UserViewResponse]:
    return await UserController(session, user).get_user()
