"""Repository selection.

One place decides which storage backend to use: SQL when ``DATABASE_URL`` is
configured, otherwise in-memory. Keeping this isolated means the rest of the app
is unaware of the choice.
"""

from __future__ import annotations

from app.core.config import Settings
from app.repositories.base import TaskRepository
from app.repositories.memory import InMemoryTaskRepository


def build_repository(settings: Settings) -> TaskRepository:
    if settings.database_url:
        # Imported lazily so SQLAlchemy is only required when actually used.
        from app.repositories.sql import SqlTaskRepository

        return SqlTaskRepository(settings.database_url)
    return InMemoryTaskRepository()
