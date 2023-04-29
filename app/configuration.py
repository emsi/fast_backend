"""Configuration module for the backend."""
import os
import secrets
from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, validator, BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastBackend"
    VERSION: str = "0.1.0"

    # 30 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    DATA_DIR: Path = Path(os.getcwd()) / "data"
    SESSIONS_DIR: Path = DATA_DIR / "sessions"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: "['http://localhost', 'http://localhost:3000', 'https://backend.example.com']"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Assemble CORS origins."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        """Read configuration from .env file."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()


class SecretKey(BaseSettings):
    secret_key: str = None

    class Config:
        """Read secret key from secure file."""
        secrets_dir = settings.DATA_DIR / "secrets"
        secret_path = secrets_dir / "secret_key"

    def __init__(self):
        # Create config dir if not exists
        os.makedirs(self.Config.secrets_dir, mode=0o700, exist_ok=True)
        super(SecretKey, self).__init__()

        if not self.secret_key:
            self.secret_key = secrets.token_urlsafe(32)
            self.Config.secret_path.touch(mode=0o700)
            self.Config.secret_path.write_text(self.secret_key)


secret_key = SecretKey().secret_key
