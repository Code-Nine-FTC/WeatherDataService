import jwt

from app.modules.security import PasswordManager, TokenManager

def test_password_hash_and_verify():
    manager = PasswordManager()
    password = "secure"
    hashed = manager.password_hash(password)
    assert manager.verify_password(password, hashed)

def test_password_hash_fail():
    manager = PasswordManager()
    hashed = manager.password_hash("password")
    assert not manager.verify_password("wrong", hashed)

def test_token_creation_with_mock_user():
    class MockUser:
        id = 123
        name = "Mock"
        email = "mock@example.com"
        is_adm = False
        is_viewer = True

    user = MockUser()
    tm = TokenManager()
    token = tm.create_access_token(user)
    decoded = jwt.decode(token, tm._TokenManager__secret_key, algorithms=[tm._TokenManager__algorithm])
    assert decoded["sub"] == str(user.id)
