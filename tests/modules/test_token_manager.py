import pytest
import jwt
from datetime import datetime
from app.modules.security import TokenManager
from app.schemas.user import UserResponse


@pytest.mark.asyncio
async def test_token_contains_user_id():
    fake_user = UserResponse(
        id=1,
        name="Test User",
        email="test@example.com",
        is_adm=False,
        is_viewer=True,
        password="hashed_password_123",
        last_update=datetime.utcnow()
    )

    token_manager = TokenManager()
    token = token_manager.create_access_token(fake_user)

    secret = token_manager._TokenManager__secret_key
    algorithm = token_manager._TokenManager__algorithm

    decoded = jwt.decode(token, secret, algorithms=[algorithm])
    assert "sub" in decoded
    assert decoded["sub"] == str(fake_user.id)
