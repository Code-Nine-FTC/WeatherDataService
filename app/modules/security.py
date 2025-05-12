from datetime import datetime, timedelta

import jwt
from pwdlib import PasswordHash
from app.config.settings import Settings
from app.schemas.user import UserResponse


class PasswordManager:
    def __init__(self) -> None:
        self.__pwd_context = PasswordHash.recommended()

    def password_hash(self, password: str) -> str:
        return self.__pwd_context.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        return self.__pwd_context.verify(password, hashed)


class TokenManager:
    def __init__(self) -> None:
        self.__settings = Settings()  # type: ignore[call-arg]
        self.__algorithm = self.__settings.ALGORITHM
        self.__secret_key = self.__settings.SECRET_KEY
        self.__access_token_expire_minutes = self.__settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: UserResponse) -> str:
        expire = datetime.now().astimezone() + timedelta(
            minutes=self.__access_token_expire_minutes
        )
        to_encode = {"sub": str(data.id), "exp": expire}
        return jwt.encode(to_encode, self.__secret_key, algorithm=self.__algorithm)
