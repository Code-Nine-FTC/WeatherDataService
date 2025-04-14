from datetime import datetime
import jwt

from app.modules.security import TokenManager

def test_token_contains_user_id_mocked():
    class FakeUser:
        id = 1
        name = "Test User"
        email = "test@example.com"
        is_adm = False
        is_viewer = True

    fake_user = FakeUser()

    token_manager = TokenManager()
    token = token_manager.create_access_token(fake_user)

    secret = token_manager._TokenManager__secret_key
    algorithm = token_manager._TokenManager__algorithm

    decoded = jwt.decode(token, secret, algorithms=[algorithm])
    assert "sub" in decoded
    assert decoded["sub"] == str(fake_user.id)
