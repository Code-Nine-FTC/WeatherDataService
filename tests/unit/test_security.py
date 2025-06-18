from app.modules.security import PasswordManager


def test_password_hash_and_verify() -> None:
    manager = PasswordManager()
    password = "secure"
    hashed = manager.password_hash(password)
    assert manager.verify_password(password, hashed)


def test_password_hash_fail() -> None:
    manager = PasswordManager()
    hashed = manager.password_hash("password")
    assert not manager.verify_password("wrong", hashed)
