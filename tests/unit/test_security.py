from datetime import datetime

import jwt

from app.modules.security import PasswordManager, TokenManager
from app.schemas.user import UserResponse


def test_password_hash_and_verify() -> None:
    manager = PasswordManager()
    password = "secure"
    hashed = manager.password_hash(password)
    assert manager.verify_password(password, hashed)


def test_password_hash_fail() -> None:
    manager = PasswordManager()
    hashed = manager.password_hash("password")
    assert not manager.verify_password("wrong", hashed)


def test_token_creation_with_mock_user() -> None:
    user = UserResponse(
        id=123,
        name="Mock",
        email="mock@example.com",
        password="hashed_password",
        last_update=datetime.utcnow(),
    )
    tm = TokenManager()
    token = tm.create_access_token(user)
    secret = getattr(tm, "secret_key", None) or getattr(tm, "_secret_key", None)
    algorithm = getattr(tm, "algorithm", None) or getattr(tm, "_algorithm", None)
    assert secret is not None
    assert algorithm is not None
    decoded = jwt.decode(token, secret, algorithms=[algorithm])
    assert decoded["sub"] == str(user.id)
