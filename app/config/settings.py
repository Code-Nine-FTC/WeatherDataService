# -*- coding: utf-8 -*-

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TEST_ENV: bool = False
    DATABASE_URL_TEST: str


settings = Settings()  # type: ignore[call-arg]
