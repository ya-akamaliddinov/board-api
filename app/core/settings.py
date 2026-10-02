from typing import Annotated

from fastapi import Depends, Request
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    name: str = "Board API"
    version: str = "1.0.0"
    debug: bool = False


class DatabaseSettings(BaseSettings):
    ulr: str


class AuthSettings(BaseSettings):
    jwt_secret: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    database_url: str
    secret: str
    minimal_post_debounce_time: int

    @property
    def app(self) -> AppSettings:
        return AppSettings()

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(url=self.database_url)

    @property
    def auth(self) -> AuthSettings:
        return AuthSettings(jwt_secret=self.secret)


def get_settings(request: Request):
    return request.app.state.settings


SettingsDeps = Annotated[Settings, Depends(get_settings)]
