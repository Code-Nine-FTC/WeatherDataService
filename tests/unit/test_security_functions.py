import jwt
import pytest

from app.modules.security import PasswordManager, TokenManager

pytestmark = pytest.mark.unit


# ---------- PasswordManager Tests ----------


def test_password_hash_returns_hashed_string() -> None:
    manager = PasswordManager()
    plain_password = "supersecret"
    hashed = manager.password_hash(plain_password)

    assert isinstance(hashed, str)
    assert hashed != plain_password


def test_verify_password_success() -> None:
    manager = PasswordManager()
    plain = "mypassword"
    hashed = manager.password_hash(plain)

    assert manager.verify_password(plain, hashed) is True


def test_verify_password_failure() -> None:
    manager = PasswordManager()
    hashed = manager.password_hash("mypassword")

    assert manager.verify_password("wrongpassword", hashed) is False


# ---------- TokenManager Tests ----------


def test_create_access_token_structure_with_mock() -> None:
    manager = TokenManager()

    class MockUser:
        id = 1

    user = MockUser()

    token = manager.create_access_token(user)  # type: ignore[arg-type]

    assert isinstance(token, str)

    secret_key = getattr(
        manager, "secret_key", getattr(manager, "_TokenManager__secret_key", "testsecret")
    )
    algorithm = getattr(
        manager, "algorithm", getattr(manager, "_TokenManager__algorithm", "HS256")
    )

    decoded = jwt.decode(token, secret_key, algorithms=[algorithm])

    assert decoded.get("sub") == str(user.id)
    assert "exp" in decoded
