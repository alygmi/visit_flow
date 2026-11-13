from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Konfigurasi aplikasi dari environment atau file .env di root repo."""

    database_url: str = (
        "postgresql+psycopg2://visitflow:visitflow@localhost:5433/visitflow"
    )
    jwt_secret: str = "dev-only-change-this-secret"
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 480
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
