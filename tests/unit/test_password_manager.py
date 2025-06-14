from app.modules.security import PasswordManager


def test_password_hash_and_verify() -> None:
    manager = PasswordManager()
    password = "senha_super_segura"
    hashed = manager.password_hash(password)
    assert manager.verify_password(password, hashed)


def test_password_verify_fails_with_wrong_password() -> None:
    manager = PasswordManager()
    password = "senha_certa"
    hashed = manager.password_hash(password)
    assert not manager.verify_password("senha_errada", hashed)
