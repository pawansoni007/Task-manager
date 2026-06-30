"""Application configuration.

Settings are read from environment variables (and an optional ``.env`` file).
Only two knobs matter for this project:

- ``DATABASE_URL``: when set, the app uses the SQL repository; otherwise it
  falls back to the in-memory repository.
- ``CORS_ORIGINS``: comma-separated list of origins allowed to call the API
  (the deployed frontend URL, plus localhost for development).
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Mini Task Tracker API"

    # When None, the in-memory repository is used.
    database_url: str | None = None

    # Comma-separated origins; defaults cover local Vite dev servers.
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (read env once per process)."""
    return Settings()
