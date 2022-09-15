from pydantic import BaseSettings
from functools import cache


class DBSettings(BaseSettings):
    username: str
    password: str
    database: str
    host: str
    port: str

    class Config:
        env_prefix = "DB_"
        env_file = ".env"


class TokenSettings(BaseSettings):
    access_secret_key: str
    refresh_secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    class Config:
        env_prefix = "TK_"
        env_file = ".env"


@cache
def get_token_settings() -> TokenSettings:
    return TokenSettings()


@cache
def get_db_settings() -> DBSettings:
    return DBSettings()
