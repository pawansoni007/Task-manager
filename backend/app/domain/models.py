"""Storage-agnostic domain model.

This ``Task`` is the single source of truth for what a task *is*, independent of
how it is stored (in-memory dict or SQL row) or exposed (Pydantic schema). Both
repositories produce and consume this type, so the service layer never has to
care about storage details.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import uuid4


class Status(str, enum.Enum):
    OPEN = "open"
    COMPLETED = "completed"


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Task:
    title: str
    description: str = ""
    status: Status = Status.OPEN
    priority: Priority | None = None
    due_date: date | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        # A freshly created task has updated_at == created_at (single instant).
        if self.updated_at is None:
            self.updated_at = self.created_at

    def touch(self) -> None:
        """Bump ``updated_at`` — called by the service on every mutation."""
        self.updated_at = _now()
