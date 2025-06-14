from datetime import datetime

import jwt
import pytest

from app.modules.security import TokenManager
from app.schemas.user import UserResponse


class FakeUser(UserResponse):
    def __init__(self) -> None:
        super().__init__(
            id=1,
            name="Test User",
            email="test@example.com",
            password="fakepassword",
            last_update=datetime.now(),
        )
        self.is_adm = False
        self.is_viewer = True


@pytest.fixture
def token_manager() -> TokenManager:
    return TokenManager()


@pytest.fixture
def fake_user() -> UserResponse:
    return FakeUser()


def test_token_contains_user_id_mocked(
    token_manager: TokenManager, fake_user: UserResponse
) -> None:
    token = token_manager.create_access_token(fake_user)
    secret = getattr(token_manager, "secret_key", None)
    algorithm = getattr(token_manager, "algorithm", None)
    assert isinstance(secret, str)
    assert isinstance(algorithm, str)
    decoded = jwt.decode(token, secret, algorithms=[algorithm])
    assert "sub" in decoded
    assert decoded["sub"] == str(fake_user.id)


def test_token_invalid_signature(token_manager: TokenManager, fake_user: UserResponse) -> None:
    token = token_manager.create_access_token(fake_user)
    wrong_secret = "wrong_secret"
    algorithm = getattr(token_manager, "algorithm", None)
    assert isinstance(algorithm, str)
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(token, wrong_secret, algorithms=[algorithm])


def test_token_missing_sub_claim(token_manager: TokenManager, fake_user: UserResponse) -> None:
    secret = getattr(token_manager, "secret_key", None)
    algorithm = getattr(token_manager, "algorithm", None)
    assert isinstance(secret, str)
    assert isinstance(algorithm, str)
    payload = {"foo": "bar"}
    token = jwt.encode(payload, secret, algorithm=algorithm)
    decoded = jwt.decode(token, secret, algorithms=[algorithm])
    assert "sub" not in decoded


def test_token_manager_create_access_token_type(
    token_manager: TokenManager, fake_user: UserResponse
) -> None:
    token = token_manager.create_access_token(fake_user)
    assert isinstance(token, str)
    assert len(token) > 0

    fake_user = FakeUser()
    token_manager = TokenManager()
    token = token_manager.create_access_token(fake_user)

    secret = getattr(token_manager, "secret_key", None)
    algorithm = getattr(token_manager, "algorithm", None)
    assert isinstance(secret, str)
    assert isinstance(algorithm, str)

    decoded = jwt.decode(token, secret, algorithms=[algorithm])
    assert "sub" in decoded
    assert decoded["sub"] == str(fake_user.id)
