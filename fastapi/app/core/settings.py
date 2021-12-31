import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    debug: bool = True

    # database
    db_name: str = "barifac"
    db_host: str = "postgres"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "password"
    db_engine: str = "postgresql+psycopg2"

    # cors
    allow_origins: list = ["http://localhost:3000"]
    allow_headers: list = ["*"]

    # JWT
    jwt_access_token_expire_sec: int = 60 * 60 * 24
    jwt_secret_key: str = (
        "9y$B&E)H@McQfTjWnZr4t7w!z%C*F-JaNdRgUkXp2s5v8x/A?D(G+KbPeShVmYq3"
    )
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = os.path.join(BASE_DIR, "fastapi.env")

    @property
    def db_url(self):
        s = Settings()
        return f"{s.db_engine}://{s.db_user}:{s.db_password}@{s.db_host}:{str(s.db_port)}/{s.db_name}"


@lru_cache
def get_env():
    return Settings()
