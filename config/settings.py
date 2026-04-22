from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
BACKEND_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"

def load_env() -> None:

    # Load root .env first, then backend/.env to allow local override if present.
    
    load_dotenv(ROOT_ENV_FILE, override=False)
    load_dotenv(BACKEND_ENV_FILE, override=True)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise ValueError(f"{name} is required")
    return value


class Settings:

    def __init__(self) -> None:
    
        load_env()

        self.database_url: str = require_env("DATABASE_URL")
        self.secret_key: str = require_env("SECRET_KEY")
        self.algorithm: str = require_env("JWT_ALGORITHM")
        self.access_token_expire_minutes: int = int(require_env("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.sql_echo: bool = require_env("SQL_ECHO").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

        if len(self.secret_key) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")


settings = Settings()
